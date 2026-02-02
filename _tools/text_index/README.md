# Text index (поиск по всем твоим текстам)

Задача: один индекс для быстрых вопросов типа:
- “дай лучшие цитаты 2014”
- “найди все тексты, где я пишу про серф/стыд/поли/Бали”
- “собери best-of по теме”

## Что индексируем

По умолчанию:
- Telegram: `data/olydaily_export/posts_md`, `data/daily2025_export/posts_md`, `data/vi_vse_nepr_export/posts_md`
- LiveJournal (clean): `data/lj_export_clean/posts_md`
- Instagram captions: `data/ig_captions_md`
- Books: `Дурге 1-2-3.txt`, `Откуда ноги растут.txt`

## 1) Собрать индекс

```bash
python3 tools/text_index/build_text_index.py --out data/text_index/index.jsonl
```

## 2) Искать по индексу

```bash
python3 tools/text_index/search_text_index.py --index data/text_index/index.jsonl --query "серф" --limit 20
```

Фильтры:
```bash
python3 tools/text_index/search_text_index.py --index data/text_index/index.jsonl --query "поли" --year 2025 --source tg_daily
```



