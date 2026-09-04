# Команды проекта

Открыть примерочную после клонирования репозитория:

```bash
open "projects/relationship_rules_carousel/build/carousel_fitting_room_v1.html"
```

После сохранения JSON из примерочной экспортировать чистые PNG и ZIP на компьютере, где подключены HQ-оригиналы:

```bash
python3 projects/relationship_rules_carousel/scripts/export_fitting_room_state.py \
  --html projects/relationship_rules_carousel/build/carousel_fitting_room_v1.html \
  --json /absolute/path/to/latest-state.json \
  --out-dir projects/relationship_rules_carousel/output/png/final \
  --zip projects/relationship_rules_carousel/output/zip/relationship-rules-final.zip \
  --resolver /absolute/path/to/media-library-original-resolver.json
```

Всегда использовать самый свежий JSON, сохранённый из примерочной.

## Последний финальный экспорт

Состояние пользователя:

```text
source/state/relationship-rules-user-2026-09-04T111017Z-v1.json
```

Результат:

```text
output/png/final-user-2026-09-04-1910/
output/zip/relationship-rules-final-user-2026-09-04-1910.zip
```

Команда воспроизведения на компьютере с HQ-оригиналами:

```bash
python3 projects/relationship_rules_carousel/scripts/export_fitting_room_state.py \
  --html projects/relationship_rules_carousel/build/carousel_fitting_room_v1.html \
  --json projects/relationship_rules_carousel/source/state/relationship-rules-user-2026-09-04T111017Z-v1.json \
  --out-dir projects/relationship_rules_carousel/output/png/final-user-2026-09-04-1910 \
  --zip projects/relationship_rules_carousel/output/zip/relationship-rules-final-user-2026-09-04-1910.zip \
  --resolver bridge/media-library-original-resolver.json \
  --expected-slides 9
```
