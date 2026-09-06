# Библиотека промптов

Промпты пишутся **по-английски** — все ведущие модели обучены преимущественно на нём и
понимают киноязык точнее. Русский допустим, но качество следования промпту ниже.

---

## 1. Универсальная структура шот-промпта

Порядок блоков важен: модели сильнее взвешивают начало.

```
[КРУПНОСТЬ] of [СУБЪЕКТ + ФИКСИРОВАННЫЙ ДЕСКРИПТОР ВНЕШНОСТИ],
[ОДНО ДЕЙСТВИЕ],
in [ЛОКАЦИЯ + ВРЕМЯ СУТОК],
[СХЕМА СВЕТА],
shot on [ОПТИКА], [ГЛУБИНА РЕЗКОСТИ],
camera [ОДНО ДВИЖЕНИЕ],
[СТИЛЬ / ПЛЁНКА / ПАЛИТРА].
```

Пример:

```
Medium shot of a woman in her early thirties, sharp jawline, dark auburn hair
pulled back, small scar above left eyebrow, wearing a grey wool coat,
slowly turning her head toward the window,
in an empty industrial workshop at dawn,
soft cold backlight through dusty windows, warm practical lamp on the left,
shot on 35mm anamorphic, shallow depth of field,
camera slow push in,
muted teal and amber palette, subtle film grain, cinematic.
```

### Правила

- **Одно действие + одно движение камеры на промпт.** «Идёт, оборачивается и садится,
  камера облетает» — гарантированный брак. Это три шота.
- **Дескриптор внешности копируется дословно** во все промпты с этим героем.
  Не пересказывать своими словами — любая перефразировка меняет лицо.
- Указывать оптику и свет явно: это то, что даёт «кино», а не слово `cinematic`.
- Не писать длиннее ~80 слов: после этого модели начинают игнорировать хвост.
- Числа модели понимают плохо («три человека» может дать пятерых) — избегать счёта.

---

## 2. Словарь киноязыка (модели его понимают)

**Крупность:** `extreme close-up`, `close-up`, `medium close-up`, `medium shot`,
`medium wide shot`, `wide shot`, `extreme wide shot`, `over-the-shoulder`, `two shot`.

**Движение камеры:** `static locked-off shot`, `slow push in`, `slow pull out`,
`pan left/right`, `tilt up/down`, `tracking shot following the subject`,
`orbit around the subject`, `handheld, subtle shake`, `crane shot rising`, `dolly zoom`.

**Свет:** `soft diffused light`, `hard directional light`, `rim light`, `backlit, silhouette`,
`golden hour`, `blue hour`, `overcast flat light`, `single practical lamp`,
`chiaroscuro, deep shadows`, `neon spill, magenta and cyan`.

**Оптика:** `shot on 24mm wide lens`, `50mm`, `85mm portrait lens`, `anamorphic lens flare`,
`shallow depth of field, bokeh`, `deep focus`, `macro lens`.

**Плёнка / фактура:** `35mm film grain`, `Kodak Portra color palette`, `desaturated`,
`high contrast`, `halation on highlights`, `vintage 16mm`.

---

## 3. Character sheet (фиксация героя)

Шаг 1 — эталонный портрет:

```
Photorealistic portrait of a [возраст]-year-old [пол], [этнотип],
[форма лица], [глаза: цвет и форма], [волосы: цвет, длина, укладка],
[отличительная примета: шрам / родинка / очки / веснушки],
neutral expression, front view, plain grey background,
soft even studio lighting, 85mm lens, shot on Kodak Portra, ultra detailed.
```

Отличительная примета обязательна — без неё лицо будет «средним» и нестабильным.

Шаг 2 — от утверждённого эталона (через reference image, **не** новым текстовым промптом),
меняя только последнюю строку:

```
same person, same face, three-quarter view left
same person, same face, profile view
same person, same face, full body standing, wearing [костюм]
same person, same face, close-up, smiling
same person, same face, back view
```

Шаг 3 — записать **дескриптор-константу** (одна строка, 12–20 слов), которая пойдёт
во все шот-промпты:

```
CHARACTER LOCK — ANNA:
"a woman in her early thirties, sharp jawline, dark auburn hair pulled back,
small scar above left eyebrow, grey wool coat"
```

---

## 4. Локации

```
LOCATION LOCK — WORKSHOP:
"a large empty industrial workshop, concrete floor, tall dusty windows,
scattered steel beams, cold blue daylight from the left"
```

Сгенерировать по 3–5 эталонных изображений локации: общий план, средний, деталь,
плюс варианты «утро / вечер / ночь». Все планы сцены оживляются из этих кадров.

---

## 5. Image-to-video (оживление утверждённого стилла)

Здесь промпт короткий — картинка уже задана, описывать её заново вредно:

```
The woman slowly turns her head toward the window.
Camera: slow push in. Subtle dust particles in the air.
Everything else remains still.
```

Фраза `everything else remains still` заметно снижает «плавание» фона.

---

## 6. Негативные промпты

Где поддерживаются:

```
deformed hands, extra fingers, warped face, morphing features,
text, watermark, logo, subtitles,
blurry, low resolution, oversaturated, plastic skin,
jump cut, multiple people, duplicate limbs
```

Где не поддерживаются — то же самое формулируется утвердительно:
`clean background, no text, hands relaxed and out of frame`.
Самый надёжный способ избежать сломанных рук — просто не помещать их в кадр.

---

## 7. Звук

**Нативное аудио (Veo-класс)** — прямо в шот-промпте:

```
Audio: distant machinery hum, footsteps on concrete, no music.
Dialogue: she says "Мы опоздали." in a low, tired voice.
```

**TTS / клонированный голос** — размечать эмоцию и паузы:

```
[тихо, устало] Мы опоздали. [пауза 0.8с] Уже ничего не изменить.
```

**Музыка (Suno/Udio-класс):**

```
Instrumental cinematic score, slow build, low strings and sparse piano,
minimal percussion entering at 0:40, melancholic but hopeful,
90 bpm, no vocals, 2 minutes.
```

---

## 8. Хуки для вертикальных нарезок

Первые 2 секунды генерируются **отдельным шотом**, а не режутся из фильма:

| Тип хука | Промпт-заготовка |
|---|---|
| Визуальный шок | `extreme close-up of [неожиданная деталь], sudden movement, high contrast` |
| Обещание | статичный кадр + крупный текст поверх на монтаже |
| Разрыв шаблона | `[обыденная сцена] where [одна невозможная деталь]` |
| Лицо в упор | `extreme close-up of [герой] looking directly into camera, silent` |

---

## 9. Чего избегать в промптах

- Слов-заклинаний без содержания: `masterpiece, best quality, 8k, trending` — на
  современных видеомоделях они не работают и съедают внимание к остальному промпту.
- Метафор и абстракций: `feeling of loneliness` → писать конкретное: `empty chair,
  single lamp, wide empty room`.
- Отрицаний внутри позитивного промпта: `not smiling` часто читается как `smiling`.
  Писать `neutral expression`.
- Смены сцены внутри одного промпта: `then she walks outside` — это следующий шот.
