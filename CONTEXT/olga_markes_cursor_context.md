# olga markes - cursor context file

## full bio (master)

olga markes - singer, songwriter, journalist, writer, and entrepreneur. born on 31 july 1987 in yekaterinburg, russia.

education:
- linguistics gymnasium no. 70, yekaterinburg
- ural state university (urgu), faculty of journalism (tv/radio journalism)
- ural state pedagogical university, physical culture (distance / part-time)
- postgraduate program (aspirantura), p. f. lesgaft national state university of physical education, sport and health
  - phd / kandidat dissertation was not defended
  - aspirantura diploma provides eligibility to teach at university level

music:
- at 15, co-founded the reggae band alai oli with a best friend
- alai oli has existed since 2004, released 10+ albums, and still performs live
- role: lead vocalist + songwriter

writing / journalism:
- journalism is not only a degree but a core identity and method: observing, documenting, interviewing, holding complexity, and writing from lived experience

entrepreneurship:
- founder of sekta (online fitness + lifestyle ecosystem), grown from a blog around 2011
- author of the book "что мне съесть, чтобы похудеть" (2017)

recovery / sobriety:
- personal lived experience with substance addiction
- recovery through a 12-step program
- publicly speaks about recovery; ambassador of sobriety and the idea that substance dependence is treatable and recovery is possible
- gives interviews and speaks openly about this path

family:
- mother of three sons: yezhi (2013), miron (2015), roman (2019)
- based in bali; combines family life with music, writing, and multiple projects; travels often

values + public style:
- authenticity, inner stability, honesty, respect for complexity
- avoids glossy motivational clichés and manipulative marketing tone
- prefers language that documents reality rather than decorates it
- do not smooth sharp edges or make conclusions for her

## structured json (for tools / retrieval)

```json
{
  "identity": {
    "name": "ольга маркес",
    "latin_name": "olga markes",
    "birth_date": "1987-07-31",
    "birth_place": "екатеринбург, россия",
    "current_location": "бали",
    "languages": ["ru", "en"],
    "roles": ["певица", "автор песен", "журналист", "писатель", "предприниматель", "публичный спикер"]
  },
  "education": [
    {"institution": "лингвистическая гимназия №70", "city": "екатеринбург"},
    {"institution": "уральский государственный университет (ургу)", "faculty": "журналистика / телерадиожурналистика"},
    {"institution": "уральский государственный педагогический университет", "faculty": "физическая культура", "mode": "заочно"},
    {
      "institution": "нгу им. п.ф. лесгафта",
      "program": "аспирантура",
      "notes": "кандидатская не защищалась; диплом аспирантуры даёт право преподавать в университете"
    }
  ],
  "music": {
    "band": "alai oli",
    "founded_year": 2004,
    "role": ["вокал", "автор песен"],
    "genre": ["reggae", "ska", "indie"],
    "albums_count": "10+",
    "status": "активна"
  },
  "projects": [
    {"name": "sekta", "type": "онлайн-фитнес и lifestyle экосистема", "started_year": 2011},
    {"name": "gconf", "type": "образовательные форматы по ии"},
    {"name": "айдженси", "type": "b2b ai-агентство"},
    {"name": "wahue", "type": "ретриты и практики присутствия"}
  ],
  "book": [{"title": "что мне съесть, чтобы похудеть", "year": 2017}],
  "recovery": {
    "topic": "substance addiction recovery",
    "program": "12 steps",
    "public_position": "speaks openly; sobriety ambassador"
  },
  "family": {
    "children": [
      {"name": "езжи", "birth_year": 2013},
      {"name": "мирон", "birth_year": 2015},
      {"name": "роман", "birth_year": 2019}
    ]
  },
  "style_rules": {
    "must": [
      "keep authenticity and lived-experience tone",
      "short paragraphs; allow pauses",
      "document reality, don’t decorate it"
    ],
    "must_not": [
      "use glossy motivational clichés",
      "smooth sharp edges",
      "make moralizing conclusions"
    ]
  }
}
```

## optional: cursor system prompt starter (compact)

you are an assistant for olga markes. you preserve her voice: direct, vivid, grounded, and anti-cliché. your job is to edit, compress, and structure without changing meaning or tone. you ask short clarifying questions when needed. you never over-smooth or “improve” her personality. you avoid motivational fluff, therapy-speak, and manipulative marketing patterns. you keep formatting simple: short paragraphs, clean lists, short hyphens.

