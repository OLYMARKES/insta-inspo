# Handoff · relationship rules carousel

This branch contains a self-contained working copy of the carousel fitting room.

## Continue on another computer

```bash
git clone --branch codex/relationship-rules-handoff https://github.com/OLYMARKES/insta-inspo.git
open "insta-inspo/projects/relationship_rules_carousel/build/carousel_fitting_room_v1.html"
```

The editor opens from `file://` and includes the approved typefaces plus the ten selected photo previews. Text, typography, colors, layout, crop, local autosave, JSON export, and JSON import remain available.

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

The GitHub handoff bundles the nine selected previews so the current carousel stays intact. The full private SMM media library and HQ originals are intentionally not committed. Reconnect the shared library before replacing photos from the full archive or producing a publication-quality HQ export.
