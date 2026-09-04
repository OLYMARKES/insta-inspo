#!/usr/bin/env python3
"""Export every slide from a saved fitting-room JSON state."""

from __future__ import annotations

import argparse
import json
import subprocess
import struct
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import Page, sync_playwright


STORAGE_KEY = "relationship_rules_carousel-production-fitter-v1"
CONTENT_REVISION = "relationship-rules-carousel-v2-cover"
EXPECTED_SIZE = (1080, 1350)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as image:
        if image.read(8) != b"\x89PNG\r\n\x1a\n":
            raise RuntimeError(f"Not a PNG: {path}")
        length = struct.unpack(">I", image.read(4))[0]
        if image.read(4) != b"IHDR" or length < 8:
            raise RuntimeError(f"Missing PNG header: {path}")
        return struct.unpack(">II", image.read(8))


def wait_for_photo(page: Page) -> None:
    page.wait_for_function(
        """() => {
          const image = document.querySelector('#canvasPhoto');
          return image && image.complete && image.naturalWidth > 0;
        }""",
        timeout=20_000,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", required=True)
    parser.add_argument("--json", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--zip", required=True)
    parser.add_argument(
        "--expected-slides",
        type=int,
        help="Expected slide count; defaults to the number of slides in the saved JSON",
    )
    parser.add_argument(
        "--resolver",
        help="Media-library original resolver JSON used to replace preview sources with HQ originals",
    )
    parser.add_argument(
        "--editor-width",
        type=float,
        default=486,
        help="CSS width of the editor canvas to preserve its exact text wrapping",
    )
    parser.add_argument(
        "--no-frame-slides",
        default="",
        help="Comma-separated slide numbers whose cover frame is hidden during export",
    )
    args = parser.parse_args()

    html = Path(args.html).expanduser().resolve()
    state_json = Path(args.json).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    zip_path = Path(args.zip).expanduser().resolve()
    editor_width = args.editor_width
    editor_height = editor_width * 5 / 4
    device_scale_factor = 2
    post_scale = EXPECTED_SIZE[0] / (editor_width * device_scale_factor)
    no_frame_slides = {
        int(value.strip())
        for value in args.no_frame_slides.split(",")
        if value.strip()
    }

    payload = json.loads(state_json.read_text(encoding="utf-8"))
    choices = payload.get("slides")
    if not isinstance(choices, list) or not choices:
        raise RuntimeError("Saved JSON contains no slides")
    expected_slides = args.expected_slides or len(choices)
    if len(choices) != expected_slides:
        raise RuntimeError(
            f"Expected {expected_slides} slides in JSON, found "
            f"{len(choices) if isinstance(choices, list) else 0}"
        )

    resolver_path = Path(args.resolver).expanduser().resolve() if args.resolver else None
    hq_sources: dict[str, str] = {}
    converted_hq_sources: dict[str, str] = {}
    if resolver_path:
        resolver_payload = json.loads(resolver_path.read_text(encoding="utf-8"))
        resolver_records = resolver_payload.get("records", {})
        for choice in choices:
            for key in ("photo", "photo2"):
                media_id = choice.get(key)
                if not isinstance(media_id, str) or not media_id.startswith("smm:"):
                    continue
                record = resolver_records.get(media_id.removeprefix("smm:"))
                local_path = record.get("localPath") if isinstance(record, dict) else None
                if not local_path:
                    raise RuntimeError(f"HQ original is unresolved for {media_id}")
                original = Path(local_path).expanduser().resolve()
                if not original.is_file():
                    raise RuntimeError(f"HQ original is missing for {media_id}: {original}")
                browser_source = original
                if original.suffix.lower() in {".heic", ".heif"}:
                    cache_dir = out_dir / "_hq-source-cache"
                    cache_dir.mkdir(parents=True, exist_ok=True)
                    browser_source = cache_dir / f"{media_id.removeprefix('smm:')}.jpg"
                    if (
                        not browser_source.exists()
                        or browser_source.stat().st_mtime < original.stat().st_mtime
                    ):
                        subprocess.run(
                            [
                                "/usr/bin/sips",
                                "-s",
                                "format",
                                "jpeg",
                                "-s",
                                "formatOptions",
                                "100",
                                str(original),
                                "--out",
                                str(browser_source),
                            ],
                            check=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                        )
                    converted_hq_sources[media_id] = str(browser_source)
                hq_sources[media_id] = browser_source.as_uri()

    state = {
        "current": 0,
        "filter": "relevant",
        "contentRevision": CONTENT_REVISION,
        "choices": choices,
    }
    state_text = json.dumps(state, ensure_ascii=False, separators=(",", ":"))

    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    exported: list[Path] = []
    page_errors: list[str] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=CHROME, headless=True)
        page = browser.new_page(
            viewport={"width": 1512, "height": 982},
            device_scale_factor=device_scale_factor,
        )
        page.on("pageerror", lambda error: page_errors.append(str(error)))
        page.add_init_script(
            script=(
                f"localStorage.setItem({json.dumps(STORAGE_KEY)},"
                f"{json.dumps(state_text, ensure_ascii=False)});"
            )
        )
        page.goto(html.as_uri(), wait_until="networkidle")
        page.wait_for_function(
            """() => {
              const label = document.querySelector('#photoCount');
              return label && !label.textContent.includes('загружаю');
            }""",
            timeout=30_000,
        )
        if hq_sources:
            page.evaluate(
                """sources => {
                  for (const photo of photos) {
                    if (sources[photo.id]) photo.src = sources[photo.id];
                  }
                  renderCanvas();
                }""",
                hq_sources,
            )
        page.evaluate("document.fonts.ready")
        page.add_style_tag(
            content="""
              #canvas {
                width: __EDITOR_WIDTH__px !important;
                height: __EDITOR_HEIGHT__px !important;
                aspect-ratio: auto !important;
                box-sizing: border-box !important;
              }
              #canvas.export-no-frame[data-cover-proposal="true"] {
                box-shadow: var(--shadow) !important;
              }
              #canvas.export-no-frame[data-cover-proposal="true"]::after {
                display: none !important;
                box-shadow: none !important;
              }
              #titleDragHandle, #bodyDragHandle,
              #titleWidthHandle, #bodyWidthHandle,
              #titleScaleHandle, #bodyScaleHandle { display: none !important; }
              #canvasPhoto, #canvasPhotoGhost,
              .carousel-slide[data-picking-photo="true"] .slide-photo.is-active-slot,
              .carousel-slide[data-picking-photo="true"] .slide-photo-ghost.is-active-slot,
              .carousel-slide[data-workflow="smm"] .canvas-headline,
              .carousel-slide[data-workflow="smm"] .canvas-copy {
                outline: none !important;
              }
            """.replace("__EDITOR_WIDTH__", f"{editor_width:g}").replace(
                "__EDITOR_HEIGHT__", f"{editor_height:g}"
            )
        )

        slide_buttons = page.locator(".slide-item")
        if slide_buttons.count() != expected_slides:
            raise RuntimeError(
                f"Expected {expected_slides} slide buttons, found {slide_buttons.count()}"
            )

        rendered_photo_sources: list[dict[str, object]] = []
        for index in range(expected_slides):
            slide_buttons.nth(index).click()
            page.locator("#canvas").evaluate(
                "(element, noFrame) => element.classList.toggle('export-no-frame', noFrame)",
                index + 1 in no_frame_slides,
            )
            wait_for_photo(page)
            source_info = page.locator("#canvasPhoto").evaluate(
                """image => ({
                  src: image.currentSrc,
                  width: image.naturalWidth,
                  height: image.naturalHeight
                })"""
            )
            rendered_photo_sources.append(
                {
                    "slide": index + 1,
                    "photo": choices[index].get("photo"),
                    **source_info,
                }
            )
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(180)
            target = out_dir / f"slide-{index + 1:02d}.png"
            raw_target = out_dir / f"slide-{index + 1:02d}.render.png"
            canvas_box = page.locator("#canvas").bounding_box()
            if not canvas_box:
                raise RuntimeError(f"Canvas is not visible on slide {index + 1}")
            page.screenshot(
                path=str(raw_target),
                type="png",
                clip={
                    "x": canvas_box["x"],
                    "y": canvas_box["y"],
                    "width": editor_width,
                    "height": editor_height,
                },
            )
            subprocess.run(
                [
                    "/usr/bin/sips",
                    "-z",
                    str(EXPECTED_SIZE[1]),
                    str(EXPECTED_SIZE[0]),
                    str(raw_target),
                    "--out",
                    str(target),
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            raw_target.unlink()
            dimensions = png_size(target)
            if dimensions != EXPECTED_SIZE:
                raise RuntimeError(
                    f"Wrong size for {target.name}: {dimensions}, expected {EXPECTED_SIZE}"
                )
            if page.locator("#photoError").evaluate(
                "element => getComputedStyle(element).display !== 'none'"
            ):
                raise RuntimeError(f"Photo failed to load on slide {index + 1}")
            exported.append(target)
            print(
                f"[OK] {target.name} · {dimensions[0]}×{dimensions[1]} · "
                f"source {source_info['width']}×{source_info['height']}"
            )
        browser.close()

    if page_errors:
        raise RuntimeError(f"Browser errors during export: {page_errors[:5]}")

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for image in exported:
            archive.write(image, arcname=image.name)

    manifest = {
        "project": payload.get("project", "relationship_rules_carousel"),
        "source_json": str(state_json),
        "source_created_at": payload.get("createdAt"),
        "source_html": str(html),
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "slide_count": len(exported),
        "dimensions": {"width": EXPECTED_SIZE[0], "height": EXPECTED_SIZE[1]},
        "render_css_size": {"width": editor_width, "height": editor_height},
        "device_scale_factor": device_scale_factor,
        "post_scale": post_scale,
        "media_source_mode": "hq-originals" if resolver_path else "editor-sources",
        "hq_resolver": str(resolver_path) if resolver_path else None,
        "hq_overrides": len(hq_sources),
        "converted_hq_sources": converted_hq_sources,
        "rendered_photo_sources": rendered_photo_sources,
        "no_frame_slides": sorted(no_frame_slides),
        "files": [image.name for image in exported],
        "zip": str(zip_path),
    }
    manifest_path = out_dir / "export-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"[OK] ZIP: {zip_path}")
    print(f"[OK] Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
