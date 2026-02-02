# Olydaily export → clean Markdown + JSON

Этот инструмент конвертирует Telegram HTML export (например `olydaily.html`) в:
- `data/olydaily_export/olydaily_clean.md` — чистый текст, сгруппированный по дням
- `data/olydaily_export/olydaily_messages.json` — структура для анализа/поиска контекста

## Запуск

Из корня workspace:

```bash
python3 tools/olydaily_export/olydaily_to_md_json.py \
  --input-html "olydaily.html" \
  --out-dir "data/olydaily_export"
```

## Что попадёт в JSON

Для каждого сообщения:
- `dt_iso`, `date`, `time`
- `from_name`
- `text` (clean)
- `links` (если были в сообщении)
- `reactions` (эмодзи → количество)
- `media` (если это media-only или есть вложение)



