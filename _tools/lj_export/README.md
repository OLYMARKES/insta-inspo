# LiveJournal exporter (public posts)

Экспортирует **все публичные посты** пользователя LiveJournal: текст + базовые метаданные.

Источник: профиль/журнал `olymarkes` — см. [LiveJournal](https://olymarkes.livejournal.com/).

## Быстрый старт

Из корня workspace:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r tools/lj_export/requirements.txt

python tools/lj_export/lj_export.py \
  --base-url https://olymarkes.livejournal.com \
  --out-dir data/lj_export \
  --save-raw-html
```

Результаты появятся в `data/lj_export/`:
- `urls.txt` — список найденных URL постов
- `posts.jsonl` — основной машиночитаемый экспорт
- `posts.csv` — таблица для Sheets/Excel
- `posts.md` — все посты склеены в один Markdown
- `raw_html/` — сырые HTML страниц постов (если включено)

## Резюмирование / докачка

Скрипт умеет продолжать: если `posts.jsonl` уже существует, он пропускает уже обработанные URL.

## Параметры

- `--base-url`: корень журнала (например `https://olymarkes.livejournal.com`)
- `--out-dir`: куда писать результаты
- `--delay`: задержка между запросами (сек), по умолчанию 0.7
- `--max-posts`: ограничить число постов для теста
- `--save-raw-html`: сохранять сырые HTML





