const EPISODES = [
  {
    date: "2026-05-31",
    title: "Оля Маркес про отношения, воспитание детей и жизнь на Бали",
    show: "Илья Рыбалко",
    kind: "Видео",
    theme: "отношения / дети / Бали",
    metric: "2 340 просмотров",
    image: "https://i.ytimg.com/vi/26JF8K52_eQ/maxresdefault.jpg",
    description: "Большой разговор с Олей Маркес про личную жизнь, отношения, воспитание детей, переезд на Бали, бизнес и путь от сложного прошлого к новой жизни.",
    links: [{ label: "YouTube", url: "https://www.youtube.com/watch?v=26JF8K52_eQ" }]
  },
  {
    date: "2026-05-08",
    title: "Как пользоваться AI в 2026, если вы не технарь?",
    show: "Дима Мацкевич",
    kind: "Видео",
    theme: "AI / повседневные инструменты",
    metric: "26 671 просмотр",
    image: "https://img.youtube.com/vi/6WEsPzHyD9k/maxresdefault.jpg",
    description: "Оля Маркес и Дима Мацкевич разбирают, как пользоваться AI в 2026 году, если вы не технарь: с чего начать, какие инструменты брать и как применять их в жизни и работе.",
    links: [{ label: "YouTube", url: "https://www.youtube.com/watch?v=6WEsPzHyD9k&t=1130s" }]
  },
  {
    date: "2026-04-08",
    title: "Оля Маркес: как обернуть зависимости и психические травмы в свою пользу?",
    show: "Коротко и по телу",
    kind: "Аудио",
    theme: "тело / зависимости / СДВГ",
    metric: "2 125 прослушиваний",
    image: "https://cdn.mave.digital/storage/podcasts/52432c57-3d68-4752-868a-196d1535ec9f/images/c8b0d301-3468-452b-a203-893f665adb2a_600.png",
    description: "Разговор о зависимостях, 12 шагах, Оземпике, полигамных отношениях и том, как особенности психики превращаются в ресурс.",
    links: [{ label: "Mave", url: "https://korotkoipotelu.mave.digital/" }, { label: "Apple", url: "https://podcasts.apple.com/ru/podcast/%D0%BE%D0%BB%D1%8F-%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%81-%D0%BA%D0%B0%D0%BA-%D0%BE%D0%B1%D0%B5%D1%80%D0%BD%D1%83%D1%82%D1%8C-%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D0%B8-%D0%B8-%D0%BF%D1%81%D0%B8%D1%85%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5-%D1%82%D1%80%D0%B0%D0%B2%D0%BC%D1%8B/id1693577630?i=1000760243974" }]
  },
  {
    date: "2025-07-08",
    title: "Тихий враг крепких отношений и как его победить",
    show: "Мацкевич: brain, love, robots",
    kind: "Видео + аудио",
    theme: "отношения / честность",
    metric: "24 192 просмотра",
    image: "https://i.ytimg.com/vi/wtSvtJOt0q8/hq720.jpg",
    description: "Дима Мацкевич, Оля Маркес и Сатья о близости, боли, честности, ритуалах пары и зрелости в отношениях.",
    links: [{ label: "YouTube", url: "https://www.youtube.com/watch?v=wtSvtJOt0q8" }, { label: "Mave", url: "https://matskevich.mave.digital/ep-46" }]
  },
  {
    date: "2025-06-13",
    title: "The Silent Killer of Relationships",
    show: "Мацкевич: brain, love, robots",
    kind: "Видео + аудио",
    theme: "relationships / Satya",
    metric: "10 072 просмотра",
    image: "https://i.ytimg.com/vi/OJ73kkbdAuI/hq720.jpg",
    description: "Англоязычная версия разговора с Satya про любовь, смелость, боль и восстановление связи.",
    links: [{ label: "YouTube", url: "https://www.youtube.com/watch?v=OJ73kkbdAuI" }, { label: "Mave", url: "https://matskevich.mave.digital/" }, { label: "Apple", url: "https://podcasts.apple.com/us/podcast/%D0%BC%D0%B0%D1%86%D0%BA%D0%B5%D0%B2%D0%B8%D1%87-brain-love-robots/id1686931500" }]
  },
  {
    date: "2025-05-16",
    title: "Йога и деньги: главное табу в индустрии?",
    show: "Мацкевич: brain, love, robots",
    kind: "Видео + аудио",
    theme: "йога / бизнес",
    metric: "14 220 прослушиваний",
    image: "https://kinescopecdn.net/b920290c-4552-4fc8-9006-c0f476262349/posters/93c7523b-9824-4178-af3c-89d43968d9e9/f1eec42e-94d9-4e51-9e1b-ce571dfa9757.jpg",
    description: "Игорь Фреш, Дима Мацкевич и Ольга Маркес о деньгах, стыде, йоге, личном бренде и устойчивом бизнесе.",
    links: [{ label: "Mave", url: "https://matskevich.mave.digital/ep-44" }, { label: "Видео", url: "https://kinescope.io/4CmGYrj8g8LE6ed1XMCxUn" }]
  },
  {
    date: "2025-03-06",
    title: "Тантра, отношения, проживание боли и секреты красоты",
    show: "Дима Мацкевич",
    kind: "Видео",
    theme: "тантра / отношения",
    metric: "47 088 просмотров",
    image: "https://img.youtube.com/vi/h_2SEZppzQs/maxresdefault.jpg",
    description: "Видеоразговор Оли Маркес и Димы Мацкевича о боли, контакте, отношениях, телесности и красоте.",
    links: [{ label: "YouTube", url: "https://www.youtube.com/watch?v=h_2SEZppzQs" }]
  },
  {
    date: "2024-11-06",
    title: "О детях без гаджетов и плюсах многодетного материнства",
    show: "Мамочки!",
    kind: "Аудио",
    theme: "дети / материнство",
    metric: "без открытой метрики",
    image: "https://is1-ssl.mzstatic.com/image/thumb/Podcasts211/v4/1b/f4/20/1bf4209d-2ddb-d8d7-b574-4d175cb18126/mza_12110451653172810570.png/600x600bb-60.jpg",
    description: "Разговор о детях, гаджетах, семейных правилах и опыте многодетности.",
    links: [{ label: "Apple", url: "https://podcasts.apple.com/ru/podcast/%D0%BE%D0%BB%D1%8F-%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%81-%D0%BE-%D0%B4%D0%B5%D1%82%D1%8F%D1%85-%D0%B1%D0%B5%D0%B7-%D0%B3%D0%B0%D0%B4%D0%B6%D0%B5%D1%82%D0%BE%D0%B2-%D0%B8-%D0%BF%D0%BB%D1%8E%D1%81%D0%B0%D1%85-%D0%BC%D0%BD%D0%BE%D0%B3%D0%BE%D0%B4%D0%B5%D1%82%D0%BD%D0%BE%D0%B3%D0%BE/id1755343202?i=1000675863837" }]
  },
  {
    date: "2024-05-11",
    title: "Whippet podcast",
    show: "Olga Markes",
    kind: "Авторский подкаст",
    theme: "уиппеты / собаки / поведение",
    metric: "10 выпусков",
    image: "https://is1-ssl.mzstatic.com/image/thumb/Podcasts221/v4/d2/b3/e0/d2b3e0d1-ea65-465d-fcc7-6de8625b54a1/mza_14961801131504210141.jpg/600x600bb.jpg",
    description: "Отдельная авторская лента Ольги Маркес про уиппетов: выбор щенка, поведение, владельцы, кормление, туалет, спорт, ветеринария и жизнь с Чарли и Виски.",
    links: [{ label: "Apple", url: "https://podcasts.apple.com/us/podcast/whippet-podcast/id1543961061" }, { label: "RSS", url: "https://cloud.mave.digital/55139" }, { label: "Telegram", url: "https://t.me/whippetpodcast" }]
  },
  {
    date: "2024-03-30",
    title: "Как справиться с тревожностью и полюбить свои страхи",
    show: "Мацкевич: brain, love, robots",
    kind: "Видео + аудио",
    theme: "тревожность / психотерапия",
    metric: "2 206 прослушиваний",
    image: "https://kinescopecdn.net/b920290c-4552-4fc8-9006-c0f476262349/posters/49665157-b1c9-4d23-8c7b-c02906def032/9c118dd5-69de-4646-8168-0ea78581be28.jpg",
    description: "Сергей Куприянов, Оля Маркес и Дима Мацкевич о страхах, тревожности, подходах в психотерапии и детях.",
    links: [{ label: "Mave", url: "https://matskevich.mave.digital/" }, { label: "Видео", url: "https://kinescope.io/wVkrQUqroHDP8oALQi2UF8" }]
  },
  {
    date: "2024-02-13",
    title: "Tantra is a dream destroyer",
    show: "Мацкевич: brain, love, robots",
    kind: "Видео + аудио",
    theme: "tantra / Pema Gitama",
    metric: "869 прослушиваний",
    image: "https://kinescopecdn.net/b920290c-4552-4fc8-9006-c0f476262349/posters/1be7af6b-cfa7-4f89-8491-bf613d425109/c14c2a7a-e518-4485-a9a2-3bb1f7714dd8.jpg",
    description: "Pema Gitama, Oly Markes and Dima Matskevich: tantric questions, wild tantra and contact practices.",
    links: [{ label: "Mave", url: "https://matskevich.mave.digital/" }, { label: "Видео", url: "https://kinescope.io/0RGWmQ3XuAbPUv7LqYFdvg" }]
  },
  {
    date: "2024-01-14",
    title: "Секс и всякое такое",
    show: "Мацкевич: brain, love, robots",
    kind: "Аудио",
    theme: "секс / отношения",
    metric: "993 прослушивания",
    image: "../assets/cover-matskevich-seks-i-vsyakoe.jpeg",
    description: "Ольга Маркес и Дмитрий Мацкевич о сексуальном желании, энергии, духовном пути и контакте в отношениях.",
    links: [{ label: "Mave", url: "https://matskevich.mave.digital/ep-23" }]
  },
  {
    date: "2024-01-11",
    title: "Ревность и божественные ноги",
    show: "Мацкевич: brain, love, robots",
    kind: "Аудио",
    theme: "ревность / близость",
    metric: "731 прослушивание",
    image: "../assets/cover-matskevich-revnost.jpeg",
    description: "Оля и Дима исследуют ревность как триггерное чувство и возможность углубляться в отношениях.",
    links: [{ label: "Mave", url: "https://matskevich.mave.digital/ep-22" }]
  },
  {
    date: "2024-01-09",
    title: "Кто, кому, что и сколько должен?",
    show: "Мацкевич: brain, love, robots",
    kind: "Аудио",
    theme: "убеждения / роли",
    metric: "895 прослушиваний",
    image: "../assets/cover-matskevich-kto-komu-chto-dolzhen.jpeg",
    description: "Разговор об убеждениях про мужчин, женщин, деньги, роли, созависимость и заботу о себе.",
    links: [{ label: "Mave", url: "https://matskevich.mave.digital/ep-21" }]
  },
  {
    date: "2023-10-02",
    title: "Свободные отношения, оргазм и тантра",
    show: "Правило 34",
    kind: "Видео + аудио",
    theme: "секс / тантра",
    metric: "151 666 просмотров",
    image: "https://img.youtube.com/vi/5iFjBL-4gGE/maxresdefault.jpg",
    description: "Большой выпуск «Правила 34» про свободные отношения, телесность, оргазм, тантру и личный опыт.",
    links: [{ label: "YouTube", url: "https://www.youtube.com/watch?v=5iFjBL-4gGE" }, { label: "Audio", url: "https://podcast.ru/1627988781" }]
  },
  {
    date: "2023-08-18",
    title: "От этого человека я бы хотела детей...",
    show: "Родила и поняла",
    kind: "Аудио",
    theme: "отношения / материнство",
    metric: "2 154 прослушивания",
    image: "https://cdn.mave.digital/storage/podcasts/cefc1282-9cab-40ed-b94d-0017301e4efc/images/a7eeeb07-85a2-4a34-aada-1303c3481914_600.jpg",
    description: "Оля Маркес про равенство в родительстве, зависимость в отношениях, расставание и выбор отца ребенку.",
    links: [{ label: "Mave", url: "https://sektamama.mave.digital/" }, { label: "Apple", url: "https://podcasts.apple.com/us/podcast/%D1%80%D0%BE%D0%B4%D0%B8%D0%BB%D0%B0-%D0%B8-%D0%BF%D0%BE%D0%BD%D1%8F%D0%BB%D0%B0/id1672300298" }]
  },
  {
    date: "2023-07-21",
    title: "Как не сойти с ума среди родителей, которые лучше тебя",
    show: "Родила и поняла",
    kind: "Аудио",
    theme: "родительство / вина",
    metric: "2 393 прослушивания",
    image: "https://cdn.mave.digital/storage/podcasts/cefc1282-9cab-40ed-b94d-0017301e4efc/images/a7eeeb07-85a2-4a34-aada-1303c3481914_600.jpg",
    description: "О решении завести ребенка, страхе, вине, радости в материнстве и сравнении себя с другими родителями.",
    links: [{ label: "Apple", url: "https://podcasts.apple.com/dk/podcast/10-%D0%BE%D0%BB%D1%8F-%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%81-%D0%BE-%D1%82%D0%BE%D0%BC-%D0%BA%D0%B0%D0%BA-%D0%BD%D0%B5-%D1%81%D0%BE%D0%B9%D1%82%D0%B8-%D1%81-%D1%83%D0%BC%D0%B0-%D1%81%D1%80%D0%B5%D0%B4%D0%B8-%D1%80%D0%BE%D0%B4%D0%B8%D1%82%D0%B5%D0%BB%D0%B5%D0%B9/id1672300298?i=1000621882264" }]
  },
  {
    date: "2023-03-06",
    title: "Оля Маркес про свой путь, травму и творчество",
    show: "Подкаст Вани Замесина",
    kind: "Аудио",
    theme: "травма / творчество",
    metric: "4 869 прослушиваний",
    image: "https://is1-ssl.mzstatic.com/image/thumb/Podcasts211/v4/45/18/83/45188322-2bbc-0d75-bc84-db01f7ff8bd9/mza_12054557121483517142.jpg/600x600bb.jpg",
    description: "Про травму смерти мамы, аутентичность, #SEKTA, творчество, ответственность и служение.",
    links: [{ label: "SoundStream", url: "https://soundstream.media/clip/olya-markes-pro-svoy-put-travmu-i-tvorchestvo" }]
  },
  {
    date: "2022-11-30",
    title: "Какой год, такой подкаст: разговор с Ольгой Маркес",
    show: "Моя история, твоя история",
    kind: "Аудио",
    theme: "год / личная история",
    metric: "без открытой метрики",
    image: "https://pbcdn1.podbean.com/imglogo/image-logo/2035774/lena-degtyar-podcast.jpg",
    description: "Мини-серия и разговор с Ольгой Маркес о прожитом годе, поворотах и личном опыте.",
    links: [{ label: "SoundStream", url: "https://soundstream.media/clip/mini-seriya-kakoy-god-takoy-podkast-razgovor-s-ol-goy-markes" }]
  },
  {
    date: "2022-10-21",
    title: "Отношения с телом",
    show: "re-feel podcast",
    kind: "Аудио",
    theme: "тело / спорт",
    metric: "без открытой метрики",
    image: "https://cdn.mave.digital/storage/podcasts/e9711868-f25f-4052-93ef-905d6f752295/images/2f45c3eb-b25e-4bea-b40b-3974e9defdee.jpg",
    description: "О том, как работать над собой постоянно и по любви, через контакт с телом и бережность.",
    links: [{ label: "SoundStream", url: "https://soundstream.media/clip/otnosheniya-s-telom-kak-rabotat-nad-soboy-postoyanno-i-po-lyubvi-uznayem-u-oli-markes" }]
  },
  {
    date: "2022-08-03",
    title: "Об опыте ретрита: Оля Маркес и Дмитрий Мацкевич",
    show: "Эмоциональная гранулярность",
    kind: "Видео + аудио",
    theme: "ретрит / тантра",
    metric: "10 254 прослушивания",
    image: "https://img.youtube.com/vi/fS-wk8mZc9g/maxresdefault.jpg",
    description: "О совместном тантрическом ретрите, ревности, боли, проживании эмоций и практиках контакта.",
    links: [{ label: "Mave", url: "https://granularity.mave.digital/ep-9" }, { label: "YouTube", url: "https://www.youtube.com/watch?v=fS-wk8mZc9g" }]
  },
  {
    date: "2022-06-27",
    title: "Продуктивность, дзен, материнство и книги",
    show: "Терминальное чтиво",
    kind: "Видео + аудио",
    theme: "книги / жизнь",
    metric: "53 549 просмотров",
    image: "https://img.youtube.com/vi/rOPNHhidBxc/maxresdefault.jpg",
    description: "Оля Маркес / Alai Oli в разговоре о книгах, продуктивности, материнстве и личной философии.",
    links: [{ label: "YouTube", url: "https://www.youtube.com/watch?v=rOPNHhidBxc" }, { label: "Podtail", url: "https://podtail.com/ru/podcast/%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5-%D1%87%D1%82%D0%B8%D0%B2%D0%BE/--alai-oli-15-03/" }]
  },
  {
    date: "2022-03-08",
    title: "Еще один выпуск из мирного времени. Про ЗОЖ",
    show: "Сперва роди",
    kind: "Аудио",
    theme: "ЗОЖ / тело / родительство",
    metric: "без открытой метрики",
    image: "https://is1-ssl.mzstatic.com/image/thumb/Podcasts211/v4/24/17/3c/24173c08-33a0-1667-7791-f932db427717/mza_12310834449313447781.jpg/600x600bb.jpg",
    description: "Ведущие обсуждают здоровый образ жизни, удовольствие от спорта и заботу о теле; затем к разговору присоединяется Ольга Маркес как основательница Sekta.",
    links: [{ label: "Apple", url: "https://podcasts.apple.com/lv/podcast/%D0%B5%D1%89%D0%B5-%D0%BE%D0%B4%D0%B8%D0%BD-%D0%B2%D1%8B%D0%BF%D1%83%D1%81%D0%BA-%D0%B8%D0%B7-%D0%BC%D0%B8%D1%80%D0%BD%D0%BE%D0%B3%D0%BE-%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%B8-%D0%BF%D1%80%D0%BE-%D0%B7%D0%BE%D0%B6/id1455337111?i=1000553278126" }, { label: "Bookmate", url: "https://rus.bookmate.com/audiobooks/jixLaNaj" }]
  },
  {
    date: "2021-08-02",
    title: "Оля Маркес о зависимости, «Секте» и принятии своего тела",
    show: "От себя не убежишь",
    kind: "Аудио",
    theme: "зависимость / тело",
    metric: "без открытой метрики",
    image: "https://cdn.mave.digital/storage/podcasts/8c22aa40-d61c-46ee-a49b-9651b92c55d9/images/b80744cd-e6cf-4f88-9ef1-9d33b9d4bbfb.jpg",
    description: "О зависимости, #SEKTA, принятии тела и личной истории восстановления.",
    links: [{ label: "SoundStream", url: "https://soundstream.media/clip/olya-markes-o-zavisimosti-sekte-i-prinyatii-svoyego-tela" }]
  }
].sort((a, b) => new Date(b.date) - new Date(a.date));

const WHIPPET = {
  title: "Whippet podcast",
  image: "https://is1-ssl.mzstatic.com/image/thumb/Podcasts221/v4/d2/b3/e0/d2b3e0d1-ea65-465d-fcc7-6de8625b54a1/mza_14961801131504210141.jpg/600x600bb.jpg",
  photos: [
    { src: "../assets/whippet-01.png", alt: "Два уиппета на лежанке" },
    { src: "../assets/whippet-02.png", alt: "Два уиппета отдыхают на диване" },
    { src: "../assets/whippet-03.png", alt: "Уиппет на кровати" },
    { src: "../assets/whippet-04.png", alt: "Иллюстрация с уиппетом в зимней одежде" },
    { src: "../assets/whippet-05.png", alt: "Уиппет поднимается по лестнице" },
    { src: "../assets/whippet-06.png", alt: "Уиппет в зимнем комбинезоне" },
    { src: "../assets/whippet-07.png", alt: "Уиппет прячется в лежанке" },
    { src: "../assets/whippet-08.png", alt: "Уиппет в дождевике на лестнице" },
    { src: "../assets/whippet-09.png", alt: "Уиппет и ребенок дома" },
    { src: "../assets/whippet-10.png", alt: "Оля с уиппетами в массажном кресле" }
  ],
  links: [
    { label: "Apple Podcasts", url: "https://podcasts.apple.com/us/podcast/whippet-podcast/id1543961061" },
    { label: "RSS", url: "https://cloud.mave.digital/55139" },
    { label: "Telegram", url: "https://t.me/whippetpodcast" }
  ]
};

const WHIPPET_EPISODES = [
  "Путешествия с собакой и переезд",
  "Левретка это маленький уиппет?",
  "Когда пора к ветеринару? Интервью с ветеринарным врачом",
  "О заводчиках и породе. Интервью с Юлией Боровковой",
  "Зачем собаке курсинг? Интервью с Ольгой Борисовой",
  "Взросление уиппета. Команды и трюки. Истории Виски и Чарли",
  "Туалет, кормление и игрушки",
  "Щенок уиппета дома. Что дальше?",
  "Как выбрать щенка уиппета?",
  "SEASON 1 TRAILER"
].map((title, index) => ({
  title,
  image: WHIPPET.photos[index],
  url: WHIPPET.links[0].url
}));

const BASE = document.body.dataset.base || "..";
const PAGE = document.body.dataset.page || "podcast";
const dateFormat = new Intl.DateTimeFormat("ru-RU", { day: "2-digit", month: "long", year: "numeric" });
const popularTopics = ["отношения", "тело", "AI", "тревожность", "тантра", "материнство", "деньги", "зависимость", "творчество", "спорт", "книги", "собаки"];

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  }[char]));
}

function slugify(value) {
  return value.toLowerCase()
    .replace(/ё/g, "е")
    .replace(/[^a-zа-я0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 86);
}

function topicsOf(episode) {
  return episode.theme.split("/").map((item) => item.trim()).filter(Boolean);
}

function formatKey(episode) {
  if (episode.kind === "Авторский подкаст") return "author";
  if (episode.kind === "Видео + аудио") return "video-audio";
  if (episode.kind === "Видео") return "video";
  return "audio";
}

function formatLabel(key) {
  return {
    all: "Все",
    guest: "Гостевые",
    "video-audio": "Видео + аудио",
    video: "Видео",
    audio: "Аудио",
    author: "Авторские"
  }[key] || key;
}

function metricValue(episode) {
  if (/без открытой метрики/i.test(episode.metric)) return 0;
  const number = episode.metric.match(/[\d\s]+/)?.[0].replace(/\s/g, "");
  return number ? Number(number) : 0;
}

function sortEpisodes(source, sort = "popular") {
  return [...source].sort((a, b) => {
    if (sort === "newest") return new Date(b.date) - new Date(a.date);
    return metricValue(b) - metricValue(a) || new Date(b.date) - new Date(a.date);
  });
}

function normalize(episode, index) {
  const slug = `${episode.date}-${slugify(episode.title)}`;
  return {
    ...episode,
    id: slug,
    slug,
    format: formatKey(episode),
    guest: episode.kind === "Авторский подкаст" ? "Olga Markes" : episode.show,
    topics: topicsOf(episode),
    primaryUrl: `${BASE}/episodes/episode.html?slug=${encodeURIComponent(slug)}`,
    externalUrl: episode.links[0]?.url || "#",
    latest: index === 0,
    featured: [0, 1, 3, 6, 8, 14].includes(index)
  };
}

const episodes = EPISODES.map(normalize);
const libraryEpisodes = episodes.filter((episode) => episode.title !== "Whippet podcast");

function mediaMarkup(episode) {
  const image = mediaUrl(episode.image);
  return `
    <div class="media" style="--cover:url('${esc(image)}')">
      <img src="${esc(image)}" alt="Обложка выпуска: ${esc(episode.title)}" loading="lazy">
    </div>
  `;
}

function metaMarkup(episode) {
  return `<div class="meta"><span>${esc(formatLabel(episode.format))}</span><span>${prettyDate(episode.date)}</span><span>${esc(episode.show)}</span></div>`;
}

function tagsMarkup(episode, limit = 4) {
  return `<div class="tag-row">${episode.topics.slice(0, limit).map((topic) => `<span class="tag">${esc(topic)}</span>`).join("")}</div>`;
}

function prettyDate(date) {
  return dateFormat.format(new Date(`${date}T12:00:00`));
}

function mediaUrl(src) {
  if (/^(https?:|data:|file:)/.test(src)) return src;
  return new URL(src, document.baseURI).href;
}

function platformsMarkup(episode) {
  return episode.links.map((link) => `<a class="platform-link" href="${esc(link.url)}" target="_blank" rel="noopener">${esc(link.label)}</a>`).join("");
}

function episodeCard(episode) {
  return `
    <article class="episode-card">
      <a href="${episode.primaryUrl}" aria-label="Открыть выпуск: ${esc(episode.title)}">${mediaMarkup(episode)}</a>
      <div>
        ${metaMarkup(episode)}
        <h3><a href="${episode.primaryUrl}">${esc(episode.title)}</a></h3>
        <p class="episode-description clamp">${esc(episode.description)}</p>
        ${tagsMarkup(episode, 3)}
      </div>
    </article>
  `;
}

function episodeRow(episode) {
  return `
    <a class="episode-row" href="${episode.primaryUrl}">
      <div class="row-meta">${esc(formatLabel(episode.format))}<br>${prettyDate(episode.date)}<br>${esc(episode.metric)}</div>
      <div>
        <h3 class="row-title">${esc(episode.title)}</h3>
        <p class="row-desc clamp">${esc(episode.description)}</p>
        ${tagsMarkup(episode, 4)}
      </div>
      <span class="row-arrow">Открыть</span>
    </a>
  `;
}

function whippetCard(episode, index) {
  return `
    <article class="whippet-card">
      <a href="${esc(episode.url)}" target="_blank" rel="noopener" aria-label="Открыть Whippet podcast: ${esc(episode.title)}">
        <figure class="whippet-cover">
          <img src="${esc(mediaUrl(episode.image.src))}" alt="${esc(episode.image.alt)}" loading="lazy">
        </figure>
        <div class="whippet-card-body">
          <span>Episode ${String(index + 1).padStart(2, "0")}</span>
          <h3>${esc(episode.title)}</h3>
        </div>
      </a>
    </article>
  `;
}

function setupChrome() {
  const button = document.querySelector("[data-menu-button]");
  const menu = document.querySelector("[data-mobile-menu]");
  if (button && menu) {
    button.addEventListener("click", () => {
      const open = menu.classList.toggle("open");
      button.setAttribute("aria-expanded", String(open));
    });
  }

  document.querySelectorAll("[data-search-form]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const input = form.querySelector("input");
      const query = input?.value.trim();
      const target = `${BASE}/episodes/index.html${query ? `?search=${encodeURIComponent(query)}` : ""}`;
      window.location.href = target;
    });
  });
}

function renderPodcastPage() {
  const latest = libraryEpisodes[0];
  const browsable = libraryEpisodes.filter((episode) => episode.slug !== latest.slug);
  const featured = sortEpisodes(libraryEpisodes.filter((episode) => episode.featured), "popular").slice(0, 6);
  const audio = libraryEpisodes.filter((episode) => episode.format === "audio").slice(0, 8);

  document.querySelector("[data-episode-count]").textContent = libraryEpisodes.length;
  document.querySelector("[data-topic-count]").textContent = new Set(libraryEpisodes.flatMap((episode) => episode.topics.map((topic) => topic.toLowerCase()))).size;

  document.querySelector("[data-platforms]").innerHTML = [
    { label: "Все выпуски", url: `${BASE}/episodes/index.html` },
    { label: "Видео", url: `${BASE}/episodes/index.html?format=video` },
    { label: "Аудио", url: `${BASE}/episodes/index.html?format=audio` },
    { label: "Whippet podcast", url: "#whippet" }
  ].map((link) => `<a class="platform-link" href="${esc(link.url)}">${esc(link.label)}</a>`).join("");

  document.querySelector("[data-popular-topics]").innerHTML = popularTopics.map((topic) => (
    `<a class="topic-chip" href="${BASE}/episodes/index.html?topic=${encodeURIComponent(topic)}">${esc(topic)}</a>`
  )).join("") + `<a class="topic-chip" href="${BASE}/episodes/index.html">Все темы</a>`;

  document.querySelector("[data-latest]").innerHTML = `
    <article class="latest-card">
      <a class="media-link" href="${latest.primaryUrl}">${mediaMarkup(latest)}</a>
      <div class="episode-content">
        ${metaMarkup(latest)}
        <h3 class="episode-title"><a href="${latest.primaryUrl}">${esc(latest.title)}</a></h3>
        <p class="episode-description">${esc(latest.description)}</p>
        ${tagsMarkup(latest)}
        <div class="platforms" style="margin-top:20px">${platformsMarkup(latest)}<a class="button" href="${latest.primaryUrl}">Страница выпуска</a></div>
      </div>
    </article>
  `;

  document.querySelector("[data-featured]").innerHTML = featured.map(episodeCard).join("");
  renderMoreCovers("popular");
  document.querySelector("[data-whippet-links]").innerHTML = platformsMarkup(WHIPPET);
  document.querySelector("[data-whippet-episodes]").innerHTML = WHIPPET_EPISODES.map(whippetCard).join("");
  document.querySelector("[data-audio]").innerHTML = audio.map(episodeRow).join("");

  document.querySelectorAll("[data-sort-more]").forEach((button) => {
    button.addEventListener("click", () => {
      renderMoreCovers(button.dataset.sortMore);
      document.querySelectorAll("[data-sort-more]").forEach((item) => {
        item.classList.toggle("active", item === button);
      });
    });
  });

  function renderMoreCovers(sort) {
    document.querySelector("[data-more-covers]").innerHTML = sortEpisodes(browsable, sort).slice(0, 12).map(episodeCard).join("");
  }
}

function getSearchParams() {
  return new URLSearchParams(window.location.search);
}

function applyFilters(source) {
  const params = getSearchParams();
  const q = (params.get("search") || "").toLowerCase().trim();
  const format = params.get("format") || "all";
  const topic = (params.get("topic") || "all").toLowerCase();
  const sort = params.get("sort") || "newest";

  let result = source.filter((episode) => {
    const haystack = [episode.title, episode.show, episode.description, episode.kind, episode.theme, episode.metric, episode.guest, ...episode.topics].join(" ").toLowerCase();
    const matchesSearch = !q || haystack.includes(q);
    const matchesFormat = format === "all" || (format === "guest" ? episode.format !== "author" : episode.format === format);
    const matchesTopic = topic === "all" || episode.topics.some((item) => item.toLowerCase() === topic);
    return matchesSearch && matchesFormat && matchesTopic;
  });

  result = [...result].sort((a, b) => {
    if (sort === "oldest") return new Date(a.date) - new Date(b.date);
    if (sort === "az") return a.title.localeCompare(b.title, "ru");
    if (sort === "za") return b.title.localeCompare(a.title, "ru");
    return new Date(b.date) - new Date(a.date);
  });

  return result;
}

function updateUrl(next) {
  const params = getSearchParams();
  Object.entries(next).forEach(([key, value]) => {
    if (!value || value === "all" || value === "newest") params.delete(key);
    else params.set(key, value);
  });
  const query = params.toString();
  window.history.replaceState(null, "", query ? `?${query}` : window.location.pathname);
}

function renderArchivePage() {
  const params = getSearchParams();
  const topicSet = [...new Set(libraryEpisodes.flatMap((episode) => episode.topics))].sort((a, b) => a.localeCompare(b, "ru"));
  const formats = ["all", "guest", "video-audio", "video", "audio"];
  const filterWrap = document.querySelector("[data-format-filters]");
  const topicSelect = document.querySelector("[data-topic-select]");
  const sortSelect = document.querySelector("[data-sort-select]");
  const searchInput = document.querySelector("[data-archive-search]");

  filterWrap.innerHTML = formats.map((format) => `<button class="filter-pill" type="button" data-format="${format}">${formatLabel(format)}</button>`).join("");
  topicSelect.innerHTML = `<option value="all">Все темы</option>${topicSet.map((topic) => `<option value="${esc(topic)}">${esc(topic)}</option>`).join("")}`;
  topicSelect.value = params.get("topic") || "all";
  sortSelect.value = params.get("sort") || "newest";
  searchInput.value = params.get("search") || "";

  function repaint() {
    const filtered = applyFilters(libraryEpisodes);
    document.querySelector("[data-result-count]").textContent = filtered.length;
    document.querySelector("[data-episode-list]").innerHTML = filtered.length ? filtered.map(episodeRow).join("") : `<div class="empty">Ничего не найдено. Попробуй убрать часть фильтров или изменить запрос.</div>`;
    document.querySelector("[data-pagination]").innerHTML = paginationMarkup(filtered.length);
    filterWrap.querySelectorAll("[data-format]").forEach((button) => {
      button.classList.toggle("active", button.dataset.format === (getSearchParams().get("format") || "all"));
    });
  }

  filterWrap.addEventListener("click", (event) => {
    const button = event.target.closest("[data-format]");
    if (!button) return;
    updateUrl({ format: button.dataset.format });
    repaint();
  });

  topicSelect.addEventListener("change", () => {
    updateUrl({ topic: topicSelect.value });
    repaint();
  });

  sortSelect.addEventListener("change", () => {
    updateUrl({ sort: sortSelect.value });
    repaint();
  });

  document.querySelector("[data-archive-form]").addEventListener("submit", (event) => {
    event.preventDefault();
    updateUrl({ search: searchInput.value.trim() });
    repaint();
  });

  repaint();
}

function paginationMarkup(total) {
  if (!total) return "";
  return `
    <a class="page-link" href="#" aria-label="Предыдущая страница">Назад</a>
    <span class="page-link active">1</span>
    <a class="page-link" href="#">2</a>
    <a class="page-link" href="#">3</a>
    <span class="page-link" aria-hidden="true">...</span>
    <a class="page-link" href="#">Дальше</a>
  `;
}

function renderEpisodePage() {
  const slug = getSearchParams().get("slug");
  const episode = libraryEpisodes.find((item) => item.slug === slug) || libraryEpisodes[0];
  const related = libraryEpisodes.filter((item) => item.slug !== episode.slug && item.topics.some((topic) => episode.topics.includes(topic))).slice(0, 3);
  document.title = `${episode.title} | Архив подкастов Оли Маркес`;
  document.querySelector("[data-episode-detail]").innerHTML = `
    <div class="detail-grid">
      <article class="detail-main">
        ${metaMarkup(episode)}
        <h1>${esc(episode.title)}</h1>
        <p class="lead">${esc(episode.description)}</p>
        <div class="platforms">${platformsMarkup(episode)}</div>
        <div class="player-box">Здесь можно подключить YouTube, Mave или Apple embed для конкретного выпуска.</div>
        <section class="content-block" id="chapters">
          <h2>О выпуске</h2>
          <p>${esc(episode.description)} Темы выпуска: ${episode.topics.map(esc).join(", ")}.</p>
        </section>
        <section class="content-block">
          <h2>Главы</h2>
          ${["00:00 Вступление", "08:20 Основная тема", "24:10 Практические выводы", "41:30 Финальные мысли"].map((item) => {
            const [time, ...title] = item.split(" ");
            return `<div class="chapter-row"><span class="timecode">${time}</span><span>${esc(title.join(" "))}</span></div>`;
          }).join("")}
        </section>
        <section class="content-block">
          <h2>Транскрипт</h2>
          <p>Блок заложен под полный текст выпуска и поиск внутри транскрипта. Пока здесь стоит структура, чтобы позже подключить расшифровки без изменения дизайна.</p>
        </section>
        <section class="content-block">
          <h2>Похожие выпуски</h2>
          <div class="episode-list">${related.map(episodeRow).join("")}</div>
        </section>
      </article>
      <aside class="detail-sidebar">
        ${mediaMarkup(episode)}
        <div style="height:18px"></div>
        ${metaMarkup(episode)}
        <p><strong>Гость / шоу:</strong><br>${esc(episode.show)}</p>
        <p><strong>Метрика:</strong><br>${esc(episode.metric)}</p>
        ${tagsMarkup(episode)}
      </aside>
    </div>
  `;
}

setupChrome();

if (PAGE === "podcast") renderPodcastPage();
if (PAGE === "archive") renderArchivePage();
if (PAGE === "episode") renderEpisodePage();
