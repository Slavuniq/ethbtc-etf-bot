# Студия AI-креаторов: анализ рынка, конкурентов и бизнес-модели

Дата: 5 октября 2026 · Версия: v1 (черновик). Ссылки на источники — в конце документа, номера в квадратных скобках.

> Важно: содержимое Telegram-чатов (чат креаторов и чат по бизнесу) в этот анализ **не** вошло — у меня нет к ним доступа. Раздел 7 перечисляет, что именно надо проверить по чатам, чтобы довести документ до v2.

---

## 0. Резюме

1. **Рынок реальный и растёт быстрее, чем предложение качественного исполнения.** Спрос на навык «AI video generation & editing» на Upwork вырос на +329% за год — это самый быстрорастущий навык платформы [1]. 83% рекламных руководителей уже применяют AI в креативном процессе (IAB, январь 2026; два года назад — 60%) [2]. Оценки объёма AI-генерированной видеорекламы на 2026 год — порядка $9 млрд, ~12% всего digital-видео (оценка вторичных источников, см. оговорку в 1.1) [3].

2. **Арбитраж между западной ценой и украинской себестоимостью существует и большой.** Украинские AI-креаторы берут $14–45/час или ~$3 за секунду видео [4][5]; американские продакшн-агентства — $100–149/час с минимальным чеком $10–25K [6]; AI-студия Genre.ai берёт $100K за 30-секундный ролик при затратах на генерацию в несколько тысяч [7]. Между Fiverr ($75–300 за видео [8]) и Genre.ai ($100K) — огромный незанятый средний сегмент $500–25K, где и надо работать.

3. **Ваша последовательность «сначала закрытая студия-реселлер, потом открытость» — правильная.** Открытая платформа с нуля не решает вашу главную проблему (нет спроса), а добавляет две новые (холодный старт двух сторон и дезинтермедиация). Маркетплейсы берут 10–20% [9][10]; студия держит 45–60% валовой маржи и владеет клиентом. Детали — раздел 4.

4. **Деньги — не в «AI», а в двух повторяемых сегментах:** (а) performance-креативы для DTC/e-commerce брендов (Meta/TikTok ads, 10–50 вариаций в месяц, ретейнеры $2–8K/мес) и (б) product-видео для Amazon / TikTok Shop / Shopify (объём, по SKU). Кинематографичные бренд-фильмы — витрина и генератор внимания, но не базовый денежный поток: они редкие, дорогие в продаже и рискуют нарваться на backlash (Coca-Cola, McDonald's, Volvo) [11][12].

5. **Главный риск — не спрос и не исполнители, а продажи:** кто продаёт на Западе, с каким лицом, с каким английским, с каким портфолио. Второй риск — консистентность качества (эффект «меняющихся колёс у грузовиков Coca-Cola») и правовые рамки (EU AI Act ст. 50 действует с 2 августа 2026; «сырой» AI-вывод в США не защищается авторским правом) [13][14][15].

6. **Экономика (консервативно):** проект $2,500 → себестоимость креатора $800–1,000 + инструменты ~$150 → валовая маржа ~55%. Пять ретейнеров по $4K = $20K MRR при ~$10–11K валовой прибыли/мес. Реалистичная цель на 6 месяцев — 8–10 ретейнеров. Расчёты — раздел 5.

**Рекомендация:** запускать одну основную модель — **управляемую студию («Creative-as-a-Service») с нишевым позиционированием** — плюс две дешёвые пробы спроса (Upwork-агентство и «спек-ролики» для DTC-брендов). Платформу/открытость добавлять как слой **поверх уже существующего спроса** не раньше, чем будет 20+ платящих клиентов и 30+ активных креаторов. Пошаговый план — в `02-launch-playbook.md`.

---

## 1. Рынок

### 1.1 Размер и динамика

| Показатель | Значение | Источник |
|---|---|---|
| Рост спроса на навык «AI video generation & editing» на Upwork, г/г | **+329%** (самый быстрорастущий навык); AI image gen +95%; все AI-навыки +109% | Upwork In-Demand Skills 2026 [1] |
| Доля рекламных руководителей, использующих AI в креативе | **83%** (янв. 2026) против 60% двумя годами ранее | IAB via [2] |
| Рекламодатели, использующие/планирующие GenAI для видеокреатива | ~90%; 78% байеров усилят GenAI в 2026 (62% в 2025) | [3] |
| Агентства, планирующие увеличить AI-расходы в 2026 | 76% | [7] |
| Спрос на AI-fluent креативных специалистов | +144% г/г; AI Art Director +87% с 2023 | [16] |
| Глобальный спенд на AI-генерированную видеорекламу, 2026 | ~$9.1 млрд, ~12% digital-видео | [3] (оценка) |
| Стоимость: AI vs традиционное производство | ~$400 за готовую минуту vs ~$4,500; AI-короткометражки $315–750/мин | [3][17] |
| Традиционный 30-сек ролик | $10–50K, премиум $200K+ | [18] |
| US TikTok Shop, продажи 2026 | $23.4 млрд (+48% г/г), лента «забита» AI-product-видео | [19] |
| Amazon: продавцы, использовавшие AI-инструменты листингов | 400,000+; видео в листинге → до +80% конверсии | [20] |

**Оговорка по цифрам рынка.** «$9.1 млрд / 12%» и «−91% стоимости» — из агрегаторов статистики (adwave, morphed, omneky), которые сами продают AI-рекламные инструменты. Относиться как к порядку величины, не как к факту. Надёжнее всего — данные Upwork (первичные), IAB и eMarketer.

**Вывод.** Рынок на стадии «ранний массовый спрос»: покупатели уже хотят, но не умеют сами и не знают, кому доверить. Это окно 12–24 месяца, пока (а) инструменты не упростятся до «кнопки» для low-end и (б) крупные агентства не достроят собственные AI-студии (уже идёт: R/GA купила Addition, AI Digital купила барселонское агентство под свою AI Creative Studio, Promise купила школу Curious Refuge ради кадрового пайплайна) [21][22][23].

### 1.2 Кто покупает, что и по какой цене

| Сегмент | Что покупают | Цена на западе | Частота | Где искать |
|---|---|---|---|---|
| **DTC / e-com бренды** (Meta, TikTok ads) | UGC-style и product-ads, хуки/варианты, еженедельный рефреш | $350–1,200 за 15–30-сек клип [5]; ретейнеры $2–5K (indie) / $5–50K+ (агентства) [24]; Darkroom starter $5–8K/мес за 15–25 статик + 3–5 видео [24] | Еженедельно / помесячно | Meta Ad Library (кто льёт много объявлений), Shopify-экосистема, LinkedIn (Head of Growth / Performance), DTC-сообщества |
| **Amazon / TikTok Shop / Shopify селлеры** | Listing-видео, product demo 30–90 сек | $75–300 на Fiverr [8]; $500–1,500 у агентств | По SKU, волнами (Q4, запуски) | Seller-сообщества, Amazon-агентства, аггрегаторы брендов |
| **Performance- и медиа-агентства** | White-label продакшн под их брендом | Оптовый прайс −40–70% от розницы [25] | Постоянно | LinkedIn, Clutch, прямые партнёрства |
| **Real estate** | Listing/lifestyle-видео, визуализации | $180–650 за объект [5] | По объекту | Брокеражи, агенты (US/UAE/EU) |
| **B2B SaaS / tech** | Explainer, motion, product-launch | $1,500–6,000 за проект [5] | Квартально | LinkedIn, Product Hunt |
| **Mid-market бренды** | 30-сек AI-ролик / brand film | $5–25K (пространство между Fiverr и Genre.ai) [18] | Редко, под кампании | Агентства, спек-ролики, LinkedIn |
| **Enterprise / Hollywood** | Кампании | $100K за 30 сек (Genre.ai), €200K (Dor Brothers) [7][26] | — | Не наш сегмент на старте |

### 1.3 Лестница цен — где лежит арбитраж

| Уровень | Кто | Цена | Комментарий |
|---|---|---|---|
| L0 — софт | Arcads (~$110/мес), Creatify ($39/мес; $1.65–3.90 за ролик), встроенные AI-инструменты Amazon/TikTok | центы–доллары за ролик | Коммодитизирует low-end UGC-аватары [27][20] |
| L1 — гиг-фрилансеры | Fiverr: product-видео $75–300, ad-вариации $50–150 в пачках по 5–10 | сотни $ | «Гиг за $5 умер», стартовые пакеты $75–250 [8] |
| L2 — соло-операторы AI-видео (US/EU) | $800–2,500 за видео; $2,800–14,500/мес дохода | тысячи $ | Project-based, не почасовка [5] |
| L3 — агентства | Ретейнеры $4–15K/мес; Clutch $100–149/час, минимум $10–25K | десятки тысяч $ | [6][24] |
| L4 — Creative-as-a-Service | Superside: $10–100K/мес, ARR >$110M (2025), 1,200 дизайнеров в 57 странах, оценка $400M | — | **Это и есть ваша модель в масштабе** — продажа результата, а не людей [28] |
| L5 — AI-native звёзды | Genre.ai $100K/30 сек (Nike, LVMH, Qatar Airways, Oracle, Popeyes, Ramp, Google, Disney); Dor Brothers €200K за кампанию, $1M+ выручки, 100M+ просмотров | сотни тысяч $ | Работают на личном бренде и вирусности [7][26] |
| **Supply — Украина** | Freelancehunt: $14–15/час, «от $3 за секунду видео»; Upwork UA: $20–45/час [4][5] | — | Себестоимость 30-сек ролика ≈ $90–300 работы + кредиты инструментов |

**Арбитраж:** себестоимость 30-секундного качественного ролика силами украинского креатора — $150–400 (работа + кредиты). Розница на западе в сегменте L2–L3 — $800–3,000. Маржа 60–80% на уровне единицы до учёта продаж и менеджмента. Именно так Superside построила бизнес на $100M+ ARR: жёсткий отбор («100 из 50,000 заявок в год»), менеджер проекта как «лицо», SLA 12–48 часов, клиент никогда не торгуется с исполнителем напрямую [28].

### 1.4 Что движет и что тормозит

**Драйверы**
- Экономика: 70–90% экономии и дни вместо недель [18]. Kalshi: 15-клиповый ролик за 3 дня и ~$2,000, вышел в эфир финала NBA [29].
- Платформы сами подталкивают: TikTok Shop и Amazon поощряют AI-видео в листингах [19][20].
- Агентства не успевают: 76% планируют наращивать AI-расходы, холдинги покупают AI-студии [7][21][22].
- Кадровый голод: +144% спроса на AI-fluent креативщиков, зарплаты AI Creative Specialist $65–145K [16] — в США нанять дорого и долго, аутсорс логичен.

**Тормоза**
- **Backlash на «видимый AI»:** Coca-Cola 2025 (грузовики меняли форму и число колёс), McDonald's снял праздничный ролик, Volvo «Come Back Stronger» раскритикован; кампании Microsoft/Volvo/Puma с AI показали рост недоверия на 12% к базе [11][12]. Урок: продаём не «AI», а результат; скрываем швы, а не технологию.
- **Право:** в США «сырой» AI-вывод не охраняется, нужен существенный человеческий творческий вклад (Copyright Office, янв./март 2025; апелляционный суд DC, март 2025) [14]. EU AI Act ст. 50 — с 2 августа 2026 обязательна маркировка реалистичных синтетических людей/мест/объектов, штрафы до €15M или 3% оборота [13]. Meta требует AI Info-декларацию, TikTok — лейблы [27]. Tess.Design (маркетплейс AI-моделей с роялти художникам) закрылся в январе 2026 именно из-за юридической неопределённости [30].
- **Волатильность инструментов:** OpenAI закрыла приложение Sora в марте 2026 (сжигала ~$1M/день) — «строить на одном инструменте — строить на песке» [31]. Нужен мульти-тул стек (Veo, Kling, Runway, Midjourney, Seedance…).
- **Коммодитизация low-end:** AI-UGC аватары за $2–4 — софт; сюда не идём.

---

## 2. Конкуренты и аналоги

### 2.1 Карта

| Категория | Игроки | Модель | Цены | Что это значит для нас |
|---|---|---|---|---|
| AI-native студии (премиум) | Genre.ai (PJ Accetturo), Secret Level (Jason Zada), Dor Brothers, Promise (VC, инвестиции Google), Monks (Puma) | Проектная работа, личный бренд + вирусный контент → inbound | $100K/30 сек; €200K/кампания | Не конкуренты по цене. **Копировать механику: «спек-ролик как холодное письмо», основатель как медиа.** |
| Нишевые микростудии | Rabbithole, PhantomX (2–3 человека), Gennie (реконструкции для true-crime док) [32] | Ниша + 2–3 артиста | — | Доказательство, что 2–3 человека с нишей выживают. |
| Creative-as-a-Service | Superside (57 стран, $110M+ ARR), Design Pickle, Kimp, Darkroom | Подписка + управляемая команда, глобальный талант | $5–100K/мес | **Прямой аналог нашей модели.** Их слабость — цена и минимальные контракты ($15K/мес на год) → ниша под ними открыта. |
| AI-performance агентства | GrowthPlan (**Украина → US DTC: Ridge, Gut C**; «AI-produced, human-edited», клиент не пишет брифов) [33], Darkroom, admiral.media | Ретейнер, привязка к ROAS | $2–15K/мес | **GrowthPlan уже делает ровно вашу модель из Украины** — это валидация и ориентир. Изучить их оффер и найм (вакансии на Djinni). |
| Маркетплейсы AI-креаторов | **VOSU Marketplace** (запущен окт. 2026 поверх продукта с $5M run rate; Simone Ferretti) [34], QuickFrame by MNTN (5,000 исполнителей, 49 специальностей, привязан к рекламной платформе MNTN) [35], Zinn Hub, Videopixie | Маркетплейс + verification | Проектно | **Оба успешных примера построены поверх уже существующего спроса/продукта.** Самостоятельный маркетплейс с нуля — нет. На их supply-сторону можно выставить своих креаторов как дополнительный канал. |
| UGC-маркетплейсы (аналог механики) | Billo ($99/видео, 5,000+ креаторов, 22,000 брендов, креаторам <$100), Insense ($500–800/мес + 10–20%), Trend [9][10][36] | Пакеты видео / подписка + комиссия | $99+/видео | Показывают потолок цены за «просто видео» и то, что маржа маркетплейса непрозрачна для креаторов (жалобы на низкие выплаты). TikTok закрыл свой Creator Marketplace в апреле 2026 в пользу TikTok One [30]. |
| Софт (self-serve) | Arcads, Creatify, HeyGen, QuickFrame AI, Amazon/TikTok нативные генераторы | SaaS | $39–110/мес | Забирают low-end. Мы продаём там, где нужен вкус, консистентность и ответственность. |
| Украина | FIRST agency (первый полностью AI-ролик на нац. ТВ, июль 2025), Dream Lights AI Studio, Reface (нанимает AI-first creative producers) [37] | Агентства/студии | UA-цены | Конкуренция за лучших креаторов внутри страны усилится — удерживать людей надо не только деньгами (см. раздел 4.3). |

### 2.2 Пять игроков, на которых стоит смотреть внимательно

**Genre.ai / PJ Accetturo.** Ролик для Kalshi на финале NBA: 15 клипов, 3 дня, ~$2,000, Veo 3 + Gemini для промптов + Premiere [29]. После этого — Nike, LVMH, Qatar Airways, Disney, 300M+ просмотров, $100K за 30 секунд [7]. Механика роста: публичный процесс («как я сделал это за два дня»), спек-работы, X/LinkedIn как канал. Урок: **один вирусный кейс с узнаваемым брендом стоит дороже любого outbound.**

**The Dor Brothers.** 100M+ просмотров органики на провокационных AI-видео → $1M+ выручки от коммерческих проектов и консалтинга брендов, кампании по €200K [26]. Урок: контент-движок = отдел продаж.

**Superside.** $44.9M выручки в 2024, >$110M ARR в 2025, 1,200 дизайнеров в 57 странах, 420 enterprise-клиентов [28]. Клиент платит $10–100K/мес и получает «команду за цену одного джуна». Урок: **продавать outcome и SLA, не людей и часы; жёсткий отбор; менеджер — лицо для клиента.** Их же слабость — цена и годовые контракты — наша возможность в mid-market.

**GrowthPlan (Украина).** Делает performance-креативы для US DTC (Ridge, Gut C): «каждый креатив AI-produced и human-edited, построен на исследовании аудитории; клиент не трогает инструменты и не пишет брифы» [33]. Урок: **именно так формулируется оффер для DTC** — не «AI-видео», а «готовые к запуску креативы на Meta/TikTok без вашего участия».

**VOSU.** Сначала продукт для креаторов с $5M run rate — потом маркетплейс (октябрь 2026). Тезис основателя: «модели становятся изобилием, дефицит — вкус, сторителлинг и надёжное исполнение» [34]. Урок: платформа появляется **после** того, как есть и спрос, и доверие.

### 2.3 Сигналы консолидации (путь к exit)

R/GA — первая покупка за 50 лет — AI-разработчик кампаний Addition [21]. AI Digital купила барселонское креативное агентство, чтобы усилить «human intelligence» в своей AI Creative Studio (май–июль 2026) [22]. Promise купила Curious Refuge (4,000+ выпускников) ради талантов [23]. Значит, через 2–3 года работающая студия с базой клиентов и отобранной «скамейкой» креаторов — покупаемый актив для агентств и холдингов.

---

## 3. Что работает, а что нет

### 3.1 Работает

| Паттерн | Пример | Почему |
|---|---|---|
| Основатель/креатор как медиа + спек-ролики для известных брендов | Genre.ai, Dor Brothers | Доверие покупают глазами; inbound конвертирует 14.6% против 1.7% у outbound [38] |
| Управляемый сервис с подпиской и SLA, глобальный талант | Superside | Предсказуемая выручка, маржа на арбитраже, клиент не видит и не переманивает исполнителя |
| Performance-креативы для DTC с привязкой к метрикам | GrowthPlan, Darkroom | Еженедельная потребность, легко доказать ROI (CTR/ROAS), естественный ретейнер |
| Узкая ниша | Gennie (true crime), real estate, Amazon-листинги | Экспертиза ниши > экспертиза инструмента; меньше конкуренция, выше цена |
| «AI внутри, но не на упаковке» | Puma/Monks сделали за 5 недель, но продают «спот», не «AI» | Избегает backlash, фокус на результате |
| Маркетплейс поверх существующего спроса | QuickFrame (внутри MNTN), VOSU (после продукта) | Решена проблема холодного старта |

### 3.2 Не работает

| Антипаттерн | Пример | Почему |
|---|---|---|
| Открытый маркетплейс с нуля без собственного спроса | TikTok Creator Marketplace закрыт; NFT/art-маркетплейсы (Foundation, Nifty Gateway, Exchange Art) закрылись в 2026 [30] | Холодный старт двух сторон, комиссии 10–20% не покрывают CAC, стороны уходят «в личку» |
| «AI» как заголовок для массового потребителя | Coca-Cola 2025, McDonald's, Volvo [11][12] | Недоверие +12%, вирусная критика, ролики снимают |
| Строить на одном инструменте | Sora закрыт в марте 2026 [31] | Инструменты умирают/меняют цены и условия |
| Агентский пайплайн через Fiverr | «Если строите агентство > $5K/мес, Fiverr — ловушка» [39] | 20% комиссия + 5.5% с покупателя, низкий чек, нет отношений с клиентом; Fiverr Pro — только для индивидуалов |
| Продажа AI-лицензий/моделей без юр. ясности | Tess.Design закрыт [30] | Корпоративные клиенты не берут неразрешённый правовой риск |
| Low-end UGC-аватары | Arcads/Creatify за $2–4 | Софт делает это сам |

### 3.3 Серые зоны (можно, но осторожно)

- **Кинематографичные бренд-фильмы** — отличная витрина (как у Manokhina в лендингах этого репо: 573K лайков на «Avatar BTS»), но для клиентских работ нельзя использовать чужие киновселенные и лица — это только для органики.
- **Реалистичные синтетические люди/отзывы** — в EU с августа 2026 обязательна маркировка; FTC: нельзя изображать опыт, которого не было [13][40]. AI-UGC для EU/US клиентов делать только как «явный актёр/аватар», без фальшивых testimonials.
- **Kling Basic не даёт коммерческих прав; Midjourney — только платные планы, при выручке клиента >$1M/год нужны Pro/Mega; Runway — права есть на всех планах, но тренируется на ваших данных вне enterprise** [41]. Внутренний стандарт: креаторы работают только с планов, дающих коммерческую лицензию, и это фиксируется в договоре.

---

## 4. Разбор бизнес-моделей

### 4.1 Сравнение четырёх вариантов

| Критерий | A. Закрытая студия-реселлер | B. «Прозрачная студия» (гибрид) | C. Открытый маркетплейс | D. Продуктизированная подписка |
|---|---|---|---|---|
| Суть | Берём заказ под своим брендом, отдаём креатору, маржа внутри | То же, но креаторы знают правило распределения, видят рейтинг/очередь, есть публичный ростер | Бренд сам выбирает креатора и договаривается; мы берём комиссию | Фикс-пакеты «N креативов в месяц за $X», как Superside/Design Pickle |
| Время до первых денег | 2–6 недель | 2–6 недель | 6–18 месяцев (нужна ликвидность) | 4–8 недель |
| Валовая маржа | 45–65% | 40–55% (чуть больше отдаём креаторам за лояльность) | 10–20% комиссии [9][10] | 50–65% |
| Холодный старт | Нужен только спрос | Нужен только спрос | Нужны обе стороны одновременно | Нужен спрос |
| Риск дезинтермедиации | Низкий (клиент не знает исполнителя) | Средний (ростер публичен → non-solicit в договорах) | Высокий (уходят в личку после 1-й сделки) | Низкий |
| Что надо уметь | Продажи + продюсирование + QA | То же + community management | Продукт, маркетинг двух сторон, trust & safety, платежи | Продажи + операционная дисциплина (SLA, очередь) |
| Удержание креаторов | Среднее (деньги) | Высокое (деньги + прозрачность + статус) | Низкое (конкурируют по цене) | Среднее |
| Защищённость | Клиентские отношения, кейсы | + бренд среди креаторов (supply moat) | Сетевой эффект — только при масштабе | Процесс + бренд |
| Вердикт | **Старт здесь** | **Переход сюда через 3–6 мес.** | Не раньше 20+ клиентов и 30+ креаторов; как слой поверх A/B | **Основной формат продажи внутри A/B** |

### 4.2 Почему платформа с нуля — нет (аргументы для чата)

1. **У вас есть одна сторона (креаторы) и нет второй (бренды).** Платформа ценна только ликвидностью. Пока спроса нет, «витрина работ» — это просто сайт-портфолио, который никто не находит.
2. **Комиссионная экономика не сходится на малых объёмах.** 15% от $1,000 заказа = $150. Привлечь одного западного клиента холодным способом стоит $300–1,500 (время/реклама). Студия с маржой $500 на том же заказе окупает привлечение с первой сделки.
3. **Дезинтермедиация.** После первого заказа бренд и креатор знают друг друга. Upwork/Fiverr удерживают стороны эскроу, рейтингами и юр. рычагами — у вас этого не будет.
4. **Доказательства рынка:** TikTok закрыл свой Creator Marketplace; VOSU и QuickFrame запустили маркетплейсы только поверх уже существующего спроса [30][34][35].
5. **Это другой бизнес.** Маркетплейс — продуктовая компания (разработка, trust & safety, платежи, маркетинг двух сторон). Студия — сервисная (продажи, продюсирование). Запускать оба одновременно командой из нескольких человек — распылиться.

### 4.3 Как закрыть запрос чата на «открытость», не теряя маржу

Открытость, которую просят креаторы, — обычно не про «бренды видят нас напрямую», а про **доверие: сколько реально заплатил клиент и почему я получил столько.** Это решается правилами, а не маркетплейсом — «открытая кухня» внутри закрытой студии:

- **Публичное правило распределения.** Например: креатор получает **55% от цены проекта** (при ретейнере — от доли ретейнера, приходящейся на его работу); студия 45% покрывает продажи, менеджмент, QA, платежи (3–6%), налоги, риск неоплаты и правки по вине процесса. Цифра обсуждается, но она одна для всех и опубликована в чате.
- **Креатор видит цену клиента** по своему проекту (не по всем). Никаких «тайных» наценок.
- **Referral-бонус 10%** от первого года выручки клиента тому, кто его привёл — так креаторы становятся продавцами, а не конкурентами.
- **Уровни:** Trainee → Core → Lead (Lead ведёт 2–3 Trainee, получает +5–10% с их проектов). Это одновременно QA-слой и карьерный трек.
- **Публичный ростер на сайте студии** (имя, стиль, 3 работы) — как у Promise и Dor Brothers — но заказ всегда идёт через студию. Это и «открытость», и маркетинг.
- **Право первого отказа и выбор проектов** внутри закрытой доски задач.
- **Non-solicit** в обе стороны (креатор — клиентов студии, студия — не переманивает чужих клиентов креатора) на 12 месяцев.

Ровно это отличает «честного посредника» от «перепродавца», и это даёт удержание лучших людей, за которых уже конкурируют украинские студии (FIRST, Reface, Dream Lights).

### 4.4 «Запустить несколько моделей и посмотреть, что сработает»

Параллельно запускать стоит не модели, а **каналы спроса** внутри одной модели. Рекомендуемая конфигурация на первые 90 дней:

1. **Ядро:** студия-реселлер с продуктизированными пакетами (разделы 5 и playbook).
2. **Проба 1 — Upwork-агентство:** самый быстрый и дешёвый способ увидеть реальный спрос и цены (навык +329%). Фрилансерская комиссия 0–15% (обычно 10–13%), клиентская 5% [42]. Используем как «кран лидов», переводим на прямые ретейнеры после 1–2 проектов (в рамках правил Upwork — через 24 месяца или с выкупом; либо просто берём новых клиентов напрямую).
3. **Проба 2 — спек-ролики + LinkedIn/X:** 10 роликов для реальных DTC-брендов (без их согласия, как «вот что мы бы сделали для вас») → публикация + личная отправка. Это тест inbound-механики Genre/Dor в нашем масштабе.

Платформу — в бэклог с явным триггером (п. 4.1). Ещё одна ошибка — запускать одновременно курс/академию и студию под одной командой: это разные воронки. Но курс (лендинги AI Cinema Academy в этом репо) может быть **источником новых креаторов** для студии — пайплайн как у Promise + Curious Refuge.

---

## 5. Юнит-экономика

Допущения: ставка креатора (Украина) $25–35/час-эквивалент при проектной оплате; кредиты инструментов $100–250 на проект; платёжные издержки 3–6%; продюсер/QA — 10% времени на проект.

### 5.1 Единица — проект

| Пакет | Цена клиенту | Креатор (55%) | Инструменты | Платежи/прочее (5%) | Валовая прибыль | Маржа |
|---|---|---|---|---|---|---|
| «Pilot»: 3 × 15–30-сек ad + 6 вариаций хуков, 72 ч | $1,500 | $825 | $120 | $75 | $480 | 32% |
| «Launch kit»: 6 роликов + 15 вариаций + статики | $3,500 | $1,925 | $250 | $175 | $1,150 | 33% |
| «Brand film» 45–60 сек cinematic | $6,000 | $3,300 | $400 | $300 | $2,000 | 33% |
| Product-видео Amazon/TikTok Shop, пачка 10 SKU | $2,500 | $1,375 | $200 | $125 | $800 | 32% |

При доле креатора 55% маржа студии ~32–35%. Это **нижняя граница щедрости** к креаторам. Superside-подобные модели живут на 50–65%: при доле креатора 40% маржа «Launch kit» → ~47%. Рекомендация: стартовать с **50/50 на первые 10 проектов** (нужна лояльность и скорость), затем перейти к 45% креатору на проектах и 50–55% на ретейнерах (стабильность стоит доли).

### 5.2 Единица — ретейнер

| Ретейнер | Цена/мес | Объём | Пул креаторов (50%) | Инструменты | Платежи | Валовая прибыль | Маржа |
|---|---|---|---|---|---|---|---|
| Starter | $2,500 | 8 роликов + 20 вариаций | $1,250 | $200 | $125 | $925 | 37% |
| Growth | $4,500 | 15 роликов + 40 вариаций + статики | $2,250 | $350 | $225 | $1,675 | 37% |
| Scale | $8,000 | 30 роликов + 80 вариаций, 2 креатора dedicated | $4,000 | $600 | $400 | $3,000 | 38% |

### 5.3 План по месяцам (консервативный)

| Месяц | Клиенты (проект / ретейнер) | Выручка | Валовая прибыль | Комментарий |
|---|---|---|---|---|
| 1–2 | 3 / 0 | $6K | $2K | Pilot-пакеты, кейсы, первые отзывы |
| 3–4 | 4 / 3 | $22K (за 2 мес) | $8K | Первые ретейнеры, 1 white-label партнёр |
| 5–6 | 4 / 6 | $38K (за 2 мес) | $14K | ~$20K MRR; продюсер на полставки |
| 7–12 | 10 / 10–12 | $25–50K/мес | $10–20K/мес | Lead-креаторы, ростер, решение по «открытости» |

Расходы вне COGS: инструменты студии и подписки ($300–600/мес), US-юрлицо и бухгалтерия ($150–300/мес), LinkedIn Sales Navigator ($100/мес), Upwork Connects ($50–150/мес), домен/сайт/CRM ($50–100/мес), реклама спек-роликов ($200–500/мес). Итого $900–1,800/мес. Безубыточность по cash — при ~$6–8K выручки/мес; окупаемость времени основателей — от $20K MRR.

### 5.4 Чувствительность

- **Самая важная переменная — не доля креатора, а повторяемость.** Один проектный клиент = $480–2,000 прибыли и ~10 часов продаж. Один ретейнер = $900–3,000/мес при тех же 10 часах. Всё в playbook строится вокруг конверсии «пилот → ретейнер».
- **Upwork снижает маржу на 10–18 п.п.** (комиссии обеих сторон) — поэтому это канал валидации, не базовый.
- **Курс гривны/доллара** работает на вас; **рост цен инструментов** (Veo/Kling quality-тиры) — против: закладывать кредиты в прайс как отдельную строку для cinematic-проектов.

---

## 6. Риски и как их закрыть

| Риск | Вероятность / влияние | Митигация |
|---|---|---|
| Нет продаж на Западе (язык, лицо, доверие) | Высокая / критично | «Лицо» студии с английским и присутствием на LinkedIn/X; спек-ролики; первые 5 клиентов из тёплой сети; US-юрлицо и US-телефон/адрес; отзывы на Clutch/Upwork |
| Качество/консистентность (артефакты, «лишние колёса») | Средняя / высокое | QA-чеклист до отправки; Lead-креатор проверяет Trainee; «human-edited» как стандарт; правки включены |
| Backlash клиента из-за «AI» | Средняя / среднее | Позиционирование по результату; не делать реалистичных людей там, где не нужно; маркировка по правилам платформ |
| Правовые: copyright, EU AI Act, FTC | Средняя / высокое | Договор: передаём права на то, что передаваемо, честно про AI-слой; человеческая доработка; маркировка; никаких чужих IP/лиц; работать с лицензионных планов инструментов [41] |
| Инструмент закрылся / изменил условия (кейс Sora) | Средняя / среднее | Мульти-стек, 2 альтернативы на каждый этап пайплайна |
| Креаторы уходят к клиентам или в украинские студии | Средняя / среднее | Прозрачное правило распределения, referral, уровни, non-solicit, быстрые выплаты (раз в 2 недели) |
| Платежи/валютный контроль Украины | Низкая / среднее | US LLC → Wise/Payoneer/Deel → ФОП 3 группы (5% + 1% военный сбор = 6% + ЕСВ) [43]; W-8BEN, нет US-удержания по договору 2000 г. |
| Коммодитизация low-end | Высокая / низкое для нас | Не играть в UGC-аватары за $50; держаться mid-market и ниш |
| Крупные агентства достроят AI-студии | Высокая (2–3 года) / среднее | Быть к тому моменту их white-label подрядчиком или объектом покупки (раздел 2.3) |

---

## 7. Что проверить по чатам (для v2)

Без чатов я не знаю фактов, от которых зависит выбор ниши и темп:

1. **Сколько креаторов реально готовы брать коммерческие заказы** и с каким временем отклика (не «в чате 200 человек», а «15 человек ответят за 2 часа и сдадут в срок»).
2. **Их специализация:** cinematic/brand (как Manokhina) или performance/UGC/product? От этого зависит стартовый сегмент. Моя гипотеза — большинство cinematic, а деньги в performance; тогда нужна переквалификация 5–10 человек под performance-формат (хуки, вариации, субтитры, 9:16).
3. **Реальные ставки, которые они называют** за 15/30/60-секундный ролик — чтобы откалибровать раздел 5.
4. **Есть ли у кого-то западные клиенты уже** — это первые кейсы и первые referral-сделки.
5. **Какая у кого лицензия на инструменты** (Kling Basic не годится для коммерции).
6. **Что именно они вкладывают в слово «открытость»** — доступ к брендам напрямую, прозрачность денег, или право выбирать проекты? Решения в 4.3 разные для каждого случая.
7. **Кто в команде продаёт на английском** и готов быть лицом в LinkedIn/X — это узкое место №1.
8. Аргументы чата по бизнесу «за открытость»: если там есть ссылки на конкретные платформы/кейсы — надо проверить их экономику по разделу 4.

Пришлите экспорт (Telegram → ⋮ → Export chat history → JSON или HTML) — я дополню документ разделом «Выводы из чатов» и пересчитаю экономику под реальные ставки.

---

## 8. Источники

1. [Upwork — In-Demand Skills 2026 (пресс-релиз)](https://www.upwork.com/press/releases/upworks-in-demand-skills-2026-demand-for-top-ai-skills-more-than-doubles-as-ai-is-embedded-into-everyday-work); [отчёт](https://upwork.com/research/in-demand-skills-2026)
2. [Adventure PPC — IAB: 83% advertising executives deployed AI (Jan 2026)](https://adventureppc.com/blog/ai-takes-center-stage-at-super-bowl-lx-why-2026-is-the-year-of-real-adoption-in-creative-advertising)
3. [Adwave — AI video ad statistics 2026](https://adwave.com/resources/ai-video-ad-statistics-2026); [Morphed — AI video ads statistics](https://morphed.app/stats/ai-video-ads-statistics); [Omneky — AI advertising statistics 2026](https://omneky.com/blog/ai-advertising-statistics-2026) (вторичные агрегаторы)
4. [Freelancehunt — Kling AI video creators (UA)](https://freelancehunt.com/en/freelancers/audio-video/video-creation-artificial-intelligence/kling); [пример профиля $15/ч](https://freelancehunt.com/en/freelancer/tmsvv.html); [Upwork — AI freelancers Ukraine](https://www.upwork.com/hire/ai-freelancers/ua/)
5. [BetOnAI — How much AI video freelancers make in 2026 (pricing tables)](https://betonai.net/how-much-ai-video-freelancers-actually-make-in-2026-real-income-data-across-kling-runway-sora-and-veo-6-niches-with-pricing-tables/); [Upwork job: Expert AI Visual Creator $20–45/h](https://www.upwork.com/jobs/~022067264927348980911)
6. [Clutch — Video production pricing](https://www.clutch.co/agencies/video-production/pricing); [пример профиля](https://www.clutch.co/profile/slow-clap-productions)
7. [CO/AI — «I made this in two days in my underwear»: AI studios slash production costs (Genre.ai $100K/30s; 76% agencies)](https://getcoai.com/news/i-made-this-in-like-two-days-in-my-underwear-ai-studios-slash-advertising-production-costs/); [Wrapbook — PJ Accetturo on AI-native production economics](https://www.wrapbook.com/on-production-podcast/the-real-economics-of-ai-native-production-featuring-pj-accetturo); [Feedbagel — Genre.ai CEO at Upscale](https://feedbagel.com/post/how-ai-is-turning-the-ad-industry-on-its-head)
8. [FluxNote — Sell AI video services on Fiverr 2026](https://fluxnote.io/blog/sell-ai-video-services-on-fiverr-2026); [Unilink — Best Fiverr gigs 2026](https://unil.ink/ua/blog/best-fiverr-gigs-2026); [Genra — AI video freelancer guide](https://genra.ai/blog/ai-video-freelancer-business-guide)
9. [Billo vs Insense (Billo blog)](https://billo.app/blog/billo-vs-insense/); [ContentRewards — Billo vs Insense 2026](https://contentrewards.com/articles/billo-vs-insense)
10. [MakeInfluence — Billo, Trend, Insense marketplaces](https://www.makeinfluence.com/en/academy/billo-trend-and-insense-international-ugc-content-marketplaces)
11. [RetailBoss — Coca-Cola AI holiday campaign backlash](https://retailboss.co/coca-colas-ai-generated-holiday-campaign-and-the-backlash-that-went-viral); [Tom's Guide — Coca-Cola AI Christmas ad 2025](https://tomsguide.com/ai/ai-image-video/coca-cola-turns-to-ai-for-its-christmas-ad-in-2025-sparking-mixed-reactions)
12. [DesignRush — 7 worst AI advertising backfires of 2025 (+12% distrust)](https://news.designrush.com/7-worst-ai-advertising-backfires-2025); [Creative Bloq — Volvo AI advert](https://creativebloq.com/creative-inspiration/advertising/volvos-shocking-ai-advert-looks-like-a-bad-student-project-it-couldnt-afford-to-finish); [AdAge — Puma AI ad via Monks](https://adage.com/article/digital-marketing-ad-tech-news/puma-uses-ai-agents-create-ad-agency-monks/2605866)
13. [Baker McKenzie — EU AI Act disclosure rules for marketing content](https://connectontech.bakermckenzie.com/ai-generated-marketing-content-new-eu-ai-act-disclosure-rules-and-the-uk-position/); [The Drum — AI disclosure laws EU & California](https://www.thedrum.com/news/ai-disclosure-laws-arrive-in-the-eu-and-california-what-do-they-mean-for-marketers); [Cinerads — AI ad disclosure: Meta, TikTok, YouTube, EU](https://www.cinerads.com/blog/ai-ad-disclosure-requirements)
14. [Neal & Leroy — Copyright Office 2025 AI reports → 2026](https://www.nealandleroy.com/post/taking-a-closer-look-what-the-copyright-office-s-2025-ai-reports-mean-for-2026); [MTLR — Works produced by generative AI](https://mttlr.org/?p=42162)
15. [Dynamis LLP — AI disclosure in 2026 for brands and influencers](https://dynamisllp.com/knowledge/ai-disclosure-in-2026-recent-developments-and-practical-steps-for-brands-and-influencers)
16. [Salt — AI Talent Report (creative skills)](https://welovesalt.com/insights/creative-skills-creative-jobs); [Rework — AI Creative Specialist JD 2026](https://resources.rework.com/ja/libraries/job-description-templates/ai-creative-specialist); [Mondo — Content marketing hiring 2026](https://mondo.com/insights/how-content-marketing-trends-are-shaping-hiring-for-2026/)
17. [InVideo — Cost per finished minute of AI content](https://invideo.io/faq/how-much-does-ai-generated-animated-content-cost-per/); [InVideo — AI short film production stack cost](https://invideo.io/faq/how-much-does-a-complete-ai-short-film-production-stack/)
18. [Hedra — AI-generated advertising (30s spot $10–50K)](https://hedra.com/blog/ai-generated-advertising); [AI Video Bootcamp — AI video ads guide 2026](https://aivideobootcamp.com/blog/ai-video-ads-complete-guide-2026/)
19. [Metaintro — AI avatars & TikTok Shop $23B (eMarketer)](https://www.metaintro.com/blog/ai-avatars-tiktok-shop-23-billion-creator-jobs-2026); [AI Weekly — TikTok Shop sellers turn to AI avatars](https://aiweekly.co/node/6722)
20. [CO/AI — Amazon AI seller tools](https://getcoai.com/news/amazon-launches-ai-powered-seller-tools-for-enhanced-product-listings); [GliaCloud — Amazon product video requirements 2026](https://gliacloud.com/en/blog/amazon-product-video-requirements-compliance-conversion-guide-2026-edition)
21. [CO/AI — R/GA acquires Addition](https://getcoai.com/news/i-made-this-in-like-two-days-in-my-underwear-ai-studios-slash-advertising-production-costs/)
22. [PPC Land — AI Digital buys Barcelona agency](https://ppc.land/ai-digital-buys-barcelona-agency-to-feed-a-studio-that-cuts-12-weeks-to-one/); [Pulse2 — AI Digital acquisition](https://pulse2.com/ai-digital-acquires-barcelona-creative-agency-to-expand-ai-creative-studio/amp/)
23. [Promise acquires Curious Refuge](https://www.privsource.com/acquisitions/deal/promise-acquires-curious-refuge-JOSZka); [Tubefilter — Promise development deals for AI artists](https://www.tubefilter.com/2025/02/11/promise-announces-development-deals-for-groundbreaking-ai-artists/)
24. [Motionbox — How much to charge for AI UGC ads (retainers, Darkroom tiers)](https://motionbox.io/blog/how-much-to-charge-clients-for-ai-ugc-ads); [Enrich Labs — Video marketing agency guide 2026](https://www.enrichlabs.ai/blog/video-marketing-agency-complete-guide-2026); [Admiral Media — AI creative agency pricing](https://admiral.media/ai-creative-agency-pricing/)
25. [Killerspots — White label for platforms & agencies](https://killerspots.com/industries/platforms-agencies/white-label); [Leanware — White label AI agency models](https://leanware.co/insights/white-label-ai-agency)
26. [NYT via The Nightly — How a video studio (Dor Brothers) embraced AI](https://thenightly.com.au/from/the-new-york-times/the-new-york-times-how-a-video-studio-embraced-ai-and-stormed-the-internet-c-19429091); [Calcalist — Dor Brothers](https://www.calcalistech.com/ctechnews/article/c9shfk9v9)
27. [Cometly — Best AI UGC tools (Arcads/Creatify pricing)](https://www.cometly.com/post/best-ai-tool-for-ugc-ads); [Creatify — 8 best AI UGC ad tools 2026](https://creatify.ai/es/blog/the-8-best-ai-ugc-ad-tools-in-2026)
28. [Superside pricing](https://superside.com/pricing); [Designity — Superside pricing 2026](https://www.designity.com/blog/superside-pricing); [Moonb — Superside pricing 2026](https://www.moonb.io/blog/superside-pricing); [Latka — Superside revenue](https://getlatka.com/companies/superside); [TechCrunch — Superside $30M round](https://techcrunch.com/2021/12/14/superside-nabs-30m-to-connect-and-manage-freelance-creatives-working-with-in-house-marketing-and-design-teams)
29. [MarkTechPost — Kalshi Veo 3 NBA Finals ad, 95% cost cut](https://www.marktechpost.com/2025/06/14/ai-generated-ad-created-with-googles-veo3-airs-during-nba-finals-slashing-production-costs-by-95/)
30. [Feedbagel — Tess.Design retrospective](https://feedbagel.com/post/retrospective-lessons-from-tessdesigns-ai-art-marketplace-that-paid-artists-roya); [Kapwing — Paying artists royalties for AI art](https://kapwing.com/blog/learnings-from-paying-artists-royalties-for-ai-generated-art); [TechCrunch — TikTok sunsets Creator Marketplace](https://techcrunch.com/2025/02/27/tiktok-sunsets-its-creator-marketplace-for-tiktok-one-a-broader-solution-with-ai-tools)
31. [OutlierKit — OpenAI Sora shutdown 2026](https://outlierkit.com/resources/openai-sora-shutdown-ai-video-bubble-2026/); [Artforum — Sora app is dead](https://www.artforum.com/news/openai-sora-app-is-dead-deal-with-disney-scrapped-1234746299/)
32. [Intelligent Jello — Rise of the AI film studio](https://intelligentjello.substack.com/p/rise-of-the-ai-film-studio); [Secret Level](https://www.productionlist.com/production-contact/secret-level); [Mootion — Best AI content studios 2026](https://www.mootion.com/use-cases/en/the-best-ai-content-creation-studios)
33. [Djinni — GrowthPlan (Ukraine; Ridge, Gut C)](https://djinni.co/jobs/company-growthplan)
34. [Newsfile — VOSU reaches $5M run rate, launches marketplace (Oct 2026)](https://www.newsfilecorp.com/release/316897)
35. [QuickFrame by MNTN](https://quickframe.mountain.com/); [PPC Land — QuickFrame AI launch](https://ppc.land/mntn-launches-quickframe-ai-to-create-studio-quality-ads-in-12-minutes/); [BusinessWire — MNTN acquires QuickFrame](https://www.businesswire.com/news/home/20220120005315/en/MNTN-Acquires-QuickFrame-on-Heels-of-Ryan-Reynolds%E2%80%99-Maximum-Effort-Deal)
36. [Billo — how creators get paid](https://help.billo.app/en/articles/5830098-for-creators-how-and-when-you-ll-get-paid); [Yespress — Billo 5,000+ creators, 22,000+ brands](https://yespress.io/billo)
37. [Ads of the World — First AI-generated commercial on Ukrainian TV (FIRST agency)](https://www.adsoftheworld.com/campaigns/all-in-your-hands-the-first-ai-generated-commercial-on-ukrainian-tv); [Reface — AI-first creative producer vacancy](https://www.marketingmonk.so/jobboard/jobs/ai-first-creative-producer-reface-at-reface-tn5tlp)
38. [Balistro — LinkedIn B2B lead generation 2026 (founder-led content, 14.6% vs 1.7%)](https://balistro.com/linkedin-marketing-strategies-b2b-lead-generation-2026/); [Linkboost — LinkedIn lead gen success stories 2026](https://www.linkboost.co/blog/linkedin-lead-generation-success-stories-2026/)
39. [HireInSouth — Fiverr pricing & fees 2026](https://hireinsouth.com/post/fiverr-pricing); [EarnifyHub — Fiverr Pro vs regular](https://earnifyhub.com/blog/fiverr-pro-vs-regular)
40. [Loeb & Loeb — AI-generated advertising: when disclosure is required](https://www.loeb.com/en/insights/passle/2026/08/aigenerated-advertising-when-is-disclosure-required-and-when-is-it-not-enough); [Billo — US AI disclosure laws](https://billo.app/blog/us-ai-disclosure-laws/)
41. [LicenseOrg — AI video licensing 2026 (Runway, Sora, Kling)](https://licenseorg.com/blog/ai-video-licensing-2026); [Terms.law — Midjourney commercial use 2026](https://www.terms.law/2026/01/15/midjourney-commercial-use-rights-complete-2026-guide/index.html); [Terms.law — AI commercial use FAQ](https://terms.law/FAQ/ai-tools/ai-commercial-use-faq.html)
42. [goLance — Upwork fees 2026](https://golance.com/blogs/upwork-fees-explained-2026); [Upwork — pricing](https://www.upwork.com/resources/is-upwork-free)
43. [Omnivoo — Paying Ukrainian contractors from a US company 2026](https://www.omnivoo.com/blog/paying-ukrainian-contractors-from-us-company-2026); [Yankiv — Deel и ФОП 3 группы](https://yankiv.com/deel-ta-fop-3-grupy-yak-pravylno-otrymuvaty-inozemni-platezhi/); [Zenind — Can Ukrainian citizens form a US LLC](https://www.zenind.com/help/post/can-ukrainian-citizens-form-a-us-llc-a-practical-guide-for-non-resident-founders); [Unilink — Stripe Atlas 2026](https://www.unilink.us/blog/stripe-atlas-2026)
