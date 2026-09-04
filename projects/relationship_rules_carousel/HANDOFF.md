# Handoff · relationship rules carousel

This branch contains a self-contained working copy of the carousel fitting room.

## Continue on another computer

```bash
git clone --branch codex/relationship-rules-handoff https://github.com/OLYMARKES/insta-inspo.git
open "insta-inspo/projects/relationship_rules_carousel/build/carousel_fitting_room_v1.html"
```

The editor opens from `file://` and includes the approved typefaces plus the ten selected photo previews. Text, typography, colors, layout, crop, local autosave, JSON export, and JSON import remain available.

## Latest final export

- Saved state: `source/state/relationship-rules-user-2026-09-04T111017Z-v1.json`
- PNG slides: `output/png/final-user-2026-09-04-1910/`
- ZIP: `output/zip/relationship-rules-final-user-2026-09-04-1910.zip`
- Export manifest: `output/png/final-user-2026-09-04-1910/export-manifest.json`
- QA: 9 of 9 slides checked at 1080×1350; HQ originals used.

## Current decisions

- 9 slides: cover + 8 relationship rules.
- Cover follows the large white heading from the “7 habits” carousel.
- The last slide uses Geologica.
- Unbounded is excluded from the project picker and must not be used.
- User edits saved in the browser remain local until `Сохранить JSON` is used.

## Preserve work between computers

1. Click `Сохранить JSON` in the fitting room.
2. Put the downloaded JSON into `source/state/`.
3. Commit and push that JSON to the same branch.
4. On the other computer, pull the branch and use `Восстановить JSON`.

## Media limitation

The GitHub handoff bundles the selected previews so the current carousel stays intact. The exported PNGs and ZIP above are publication-quality and were rendered from HQ originals. The full private SMM media library and the original source photos are intentionally not committed; reconnect the shared library before replacing photos or reproducing the HQ export on another computer.
