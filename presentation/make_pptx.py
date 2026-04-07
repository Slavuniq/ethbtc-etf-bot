from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

# Brand colors
NAVY = RGBColor(0x0B, 0x1F, 0x3A)
GOLD = RGBColor(0xC8, 0xA2, 0x5B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xF5, 0xF1, 0xEA)
GRAY = RGBColor(0x6B, 0x6B, 0x6B)
DARK = RGBColor(0x1A, 0x1A, 0x1A)
RED = RGBColor(0xC0, 0x39, 0x2B)
GREEN = RGBColor(0x2E, 0x8B, 0x57)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def add_bg(slide, color=WHITE):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg


def add_text(slide, text, left, top, width, height, size=18, bold=False,
             color=DARK, align=PP_ALIGN.LEFT, font="Calibri"):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.name = font
    return tb


def add_rect(slide, left, top, width, height, color):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    s.fill.solid()
    s.fill.fore_color.rgb = color
    s.line.fill.background()
    return s


def add_line_accent(slide, top, color=GOLD):
    add_rect(slide, Inches(0.5), top, Inches(1.0), Inches(0.06), color)


def header(slide, title, kicker=None):
    if kicker:
        add_text(slide, kicker.upper(), Inches(0.5), Inches(0.45),
                 Inches(12), Inches(0.35), size=12, bold=True, color=GOLD)
    add_text(slide, title, Inches(0.5), Inches(0.8), Inches(12.5),
             Inches(0.9), size=32, bold=True, color=NAVY)
    add_line_accent(slide, Inches(1.7))


# ============ SLIDE 1: COVER ============
s = prs.slides.add_slide(BLANK)
add_bg(s, NAVY)
add_rect(s, 0, Inches(6.8), SW, Inches(0.7), GOLD)
add_text(s, "PRODUCER PROPOSAL", Inches(0.7), Inches(1.0),
         Inches(12), Inches(0.4), size=14, bold=True, color=GOLD)
add_text(s, "Алевтіна Дрігант", Inches(0.7), Inches(1.6),
         Inches(12), Inches(1.2), size=54, bold=True, color=WHITE)
add_text(s, "Система масштабування курсу\n«Мистецтво говорити»",
         Inches(0.7), Inches(2.9), Inches(12), Inches(1.6),
         size=28, color=WHITE)
add_text(s, "x5 за 90 днів", Inches(0.7), Inches(4.6),
         Inches(12), Inches(0.8), size=36, bold=True, color=GOLD)
add_text(s, "Презентація для зустрічі  ·  30 хвилин",
         Inches(0.7), Inches(6.95), Inches(12), Inches(0.4),
         size=12, bold=True, color=NAVY)

# ============ SLIDE 2: WHY I'M HERE ============
s = prs.slides.add_slide(BLANK)
add_bg(s)
header(s, "Чому я тут", "Контекст")

points = [
    ("11", "потоків курсу — продукт валідовано ринком"),
    ("12K", "підписників з преміум-аудиторією (UA / EU)"),
    ("$0", "інвестицій у воронку — все продажі через DM"),
]
x = Inches(0.7)
for big, small in points:
    add_rect(s, x, Inches(2.3), Inches(4.0), Inches(2.8), LIGHT)
    add_text(s, big, x + Inches(0.3), Inches(2.5), Inches(3.6),
             Inches(1.4), size=72, bold=True, color=NAVY)
    add_text(s, small, x + Inches(0.3), Inches(3.9), Inches(3.6),
             Inches(1.1), size=14, color=DARK)
    x += Inches(4.2)

add_text(s,
    "У вас є все для x5 росту. Немає лише системи, яка це збере.",
    Inches(0.7), Inches(5.6), Inches(12), Inches(0.6),
    size=20, bold=True, color=GOLD)

# ============ SLIDE 3: 3 LEAKS ============
s = prs.slides.add_slide(BLANK)
add_bg(s)
header(s, "3 діри, де зараз втрачаються гроші", "Діагностика")

leaks = [
    ("01", "Продажі через DM",
     "70-80% людей, які хочуть купити, НЕ напишуть першими.\nВтрата ~$4 500 з кожного продаючого поста."),
    ("02", "Немає бази (Telegram / email)",
     "Instagram показує пости 5-10% підписників.\nЗ 12K вас бачать 600-1 200 людей."),
    ("03", "Один продукт = один рівень доходу",
     "Між потоками — тиша. Немає продуктів,\nякі продаються щодня на автопілоті."),
]
y = Inches(2.1)
for num, title, desc in leaks:
    add_rect(s, Inches(0.7), y, Inches(0.9), Inches(1.4), NAVY)
    add_text(s, num, Inches(0.7), y + Inches(0.25), Inches(0.9),
             Inches(0.9), size=32, bold=True, color=GOLD,
             align=PP_ALIGN.CENTER)
    add_text(s, title, Inches(1.85), y + Inches(0.05), Inches(11),
             Inches(0.5), size=20, bold=True, color=NAVY)
    add_text(s, desc, Inches(1.85), y + Inches(0.6), Inches(11),
             Inches(0.9), size=13, color=GRAY)
    y += Inches(1.65)

# ============ SLIDE 4: BEFORE / AFTER MATH ============
s = prs.slides.add_slide(BLANK)
add_bg(s)
header(s, "Що дає система: математика 12-го потоку", "Розрахунок")

# BEFORE
add_rect(s, Inches(0.7), Inches(2.1), Inches(5.8), Inches(4.6), LIGHT)
add_text(s, "ЗАРАЗ", Inches(0.9), Inches(2.25), Inches(5.4),
         Inches(0.5), size=14, bold=True, color=GRAY)
add_text(s, "$3 000 – $5 000", Inches(0.9), Inches(2.7),
         Inches(5.4), Inches(0.9), size=36, bold=True, color=DARK)
before_lines = [
    "• Охват поста: ~800 людей (5-7%)",
    "• Заявок у DM: 15-20",
    "• Купили: 10-15 учнів",
    "• Чек: $300",
    "• Канал продажу: тільки Instagram DM",
]
yy = Inches(3.7)
for line in before_lines:
    add_text(s, line, Inches(0.95), yy, Inches(5.4), Inches(0.4),
             size=13, color=GRAY)
    yy += Inches(0.5)

# AFTER
add_rect(s, Inches(6.85), Inches(2.1), Inches(5.8), Inches(4.6), NAVY)
add_text(s, "ПІСЛЯ ЗАПУСКУ СИСТЕМИ",
         Inches(7.05), Inches(2.25), Inches(5.4),
         Inches(0.5), size=14, bold=True, color=GOLD)
add_text(s, "$25 000 – $35 000", Inches(7.05), Inches(2.7),
         Inches(5.4), Inches(0.9), size=36, bold=True, color=WHITE)
after_lines = [
    "• Telegram-база: 2 000+ (охват 60%)",
    "• Reels-трафік: +3 000 нових/міс",
    "• Автоворонка з прогрівом 5-7 днів",
    "• Тарифна сітка: $297 / $497 / $1 500",
    "• Купили: 50-60 учнів",
]
yy = Inches(3.7)
for line in after_lines:
    add_text(s, line, Inches(7.1), yy, Inches(5.4), Inches(0.4),
             size=13, color=WHITE)
    yy += Inches(0.5)

add_text(s, "= один запуск приносить більше, ніж зараз 6 потоків",
         Inches(0.7), Inches(6.9), Inches(12.5), Inches(0.5),
         size=16, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

# ============ SLIDE 5: 90-DAY ROADMAP ============
s = prs.slides.add_slide(BLANK)
add_bg(s)
header(s, "Дорожня карта 90 днів", "План")

stages = [
    ("ЕТАП 1\nТижні 1-3", "ФУНДАМЕНТ",
     ["Переупаковка біо + Taplink",
      "Telegram-канал + бот",
      "Лід-магніт PDF",
      "Хайлайти ВІДГУКИ / КУРС"]),
    ("ЕТАП 2\nТижні 4-6", "ВОРОНКА",
     ["Автоворонка в Telegram",
      "Міні-курс $97 (запис)",
      "Reels-стратегія: 5/тиждень",
      "Сторінка продажу курсу"]),
    ("ЕТАП 3\nТижні 7-12", "ЗАПУСК",
     ["Прогрів 14 днів до старту",
      "Запуск 12-го потоку",
      "Premium-група $1 500",
      "Корпоративні тренінги"]),
]
x = Inches(0.7)
for kicker, title, items in stages:
    add_rect(s, x, Inches(2.1), Inches(4.0), Inches(0.9), GOLD)
    add_text(s, kicker, x + Inches(0.2), Inches(2.18),
             Inches(3.6), Inches(0.8), size=12, bold=True, color=NAVY)
    add_rect(s, x, Inches(3.0), Inches(4.0), Inches(4.0), LIGHT)
    add_text(s, title, x + Inches(0.2), Inches(3.1),
             Inches(3.6), Inches(0.6), size=22, bold=True, color=NAVY)
    yy = Inches(3.85)
    for it in items:
        add_text(s, "→ " + it, x + Inches(0.2), yy, Inches(3.7),
                 Inches(0.45), size=13, color=DARK)
        yy += Inches(0.55)
    x += Inches(4.2)

# ============ SLIDE 6: 12-MONTH FORECAST ============
s = prs.slides.add_slide(BLANK)
add_bg(s)
header(s, "Прогноз доходу на 12 місяців", "Фінансова модель")

rows = [
    ("Місяці 1-2", "Підготовка системи", "$0", LIGHT),
    ("Місяць 3", "Запуск 12-го потоку", "$25-35K", LIGHT),
    ("Місяці 4-5", "Автопродажі + корпоратив", "$10-16K", LIGHT),
    ("Місяць 6", "Запуск 13-го потоку", "$30-45K", LIGHT),
    ("Місяць 7", "Літній ретрит у Європі", "$15-25K", LIGHT),
    ("Місяці 8-9", "Автопродажі + корпоратив", "$14-24K", LIGHT),
    ("Місяць 10", "Запуск 14-го потоку", "$35-50K", LIGHT),
    ("Місяці 11-12", "Новорічний запуск", "$15-25K", LIGHT),
]
y = Inches(2.05)
for period, what, money, bg in rows:
    add_rect(s, Inches(0.7), y, Inches(9.0), Inches(0.45), bg)
    add_text(s, period, Inches(0.85), y + Inches(0.07),
             Inches(2.5), Inches(0.4), size=12, bold=True, color=NAVY)
    add_text(s, what, Inches(3.4), y + Inches(0.07),
             Inches(6.2), Inches(0.4), size=12, color=DARK)
    add_text(s, money, Inches(7.9), y + Inches(0.07),
             Inches(1.7), Inches(0.4), size=12, bold=True,
             color=GREEN, align=PP_ALIGN.RIGHT)
    y += Inches(0.5)

# Total card
add_rect(s, Inches(10.0), Inches(2.05), Inches(2.9), Inches(4.0), NAVY)
add_text(s, "РАЗОМ\nЗА РІК", Inches(10.15), Inches(2.25),
         Inches(2.6), Inches(0.9), size=14, bold=True, color=GOLD)
add_text(s, "$150K", Inches(10.15), Inches(3.3),
         Inches(2.6), Inches(0.9), size=36, bold=True, color=WHITE)
add_text(s, "—", Inches(10.15), Inches(4.0),
         Inches(2.6), Inches(0.4), size=20, bold=True, color=WHITE)
add_text(s, "$250K", Inches(10.15), Inches(4.4),
         Inches(2.6), Inches(0.9), size=36, bold=True, color=WHITE)
add_text(s, "vs зараз\n~$30-60K/рік", Inches(10.15), Inches(5.35),
         Inches(2.6), Inches(0.7), size=11, color=GOLD)

add_text(s, "Зростання x3 – x5",
         Inches(0.7), Inches(6.55), Inches(12.5), Inches(0.5),
         size=18, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

# ============ SLIDE 7: WHO DOES WHAT ============
s = prs.slides.add_slide(BLANK)
add_bg(s)
header(s, "Розподіл ролей", "Як працюємо разом")

# Alevtina
add_rect(s, Inches(0.7), Inches(2.1), Inches(6.0), Inches(4.8), LIGHT)
add_text(s, "АЛЕВТІНА", Inches(0.95), Inches(2.3),
         Inches(5.5), Inches(0.5), size=14, bold=True, color=GOLD)
add_text(s, "Експерт + обличчя", Inches(0.95), Inches(2.7),
         Inches(5.5), Inches(0.6), size=22, bold=True, color=NAVY)
items_a = [
    "Записує Reels (5/тиждень)",
    "Веде ефіри і live-уроки курсу",
    "Дає експертну глибину контенту",
    "Спілкується з преміум-учнями",
    "Час: 5-7 годин на тиждень",
]
yy = Inches(3.6)
for it in items_a:
    add_text(s, "•  " + it, Inches(0.95), yy, Inches(5.5),
             Inches(0.4), size=14, color=DARK)
    yy += Inches(0.55)

# Producer
add_rect(s, Inches(6.95), Inches(2.1), Inches(6.0), Inches(4.8), NAVY)
add_text(s, "ПРОДЮСЕР", Inches(7.2), Inches(2.3),
         Inches(5.5), Inches(0.5), size=14, bold=True, color=GOLD)
add_text(s, "Система + продажі", Inches(7.2), Inches(2.7),
         Inches(5.5), Inches(0.6), size=22, bold=True, color=WHITE)
items_p = [
    "Воронка, бот, Telegram, Taplink",
    "Контент-стратегія + монтаж",
    "Запуски курсу під ключ",
    "Аналітика, дашборди, тести",
    "Перемовини: корпоративи + B2B",
]
yy = Inches(3.6)
for it in items_p:
    add_text(s, "•  " + it, Inches(7.2), yy, Inches(5.5),
             Inches(0.4), size=14, color=WHITE)
    yy += Inches(0.55)

# ============ SLIDE 8: OFFER ============
s = prs.slides.add_slide(BLANK)
add_bg(s)
header(s, "Оффер співпраці", "Умови")

# Variant A
add_rect(s, Inches(0.7), Inches(2.1), Inches(6.0), Inches(4.9), LIGHT)
add_rect(s, Inches(0.7), Inches(2.1), Inches(6.0), Inches(0.7), GOLD)
add_text(s, "ВАРІАНТ A  ·  РЕКОМЕНДОВАНИЙ",
         Inches(0.9), Inches(2.27), Inches(5.6), Inches(0.5),
         size=13, bold=True, color=NAVY)
add_text(s, "$1 000/міс  +  20% rev share",
         Inches(0.9), Inches(3.0), Inches(5.6), Inches(0.8),
         size=22, bold=True, color=NAVY)
a_items = [
    ("Термін:", "3 місяці пілот"),
    ("KPI 1:", "Запуск 12-го потоку $25K+"),
    ("KPI 2:", "База Telegram 2 000+"),
    ("KPI 3:", "Автопродажі $5K/міс до 90-го дня"),
    ("Ризик:", "Розділений 50/50"),
]
yy = Inches(3.95)
for k, v in a_items:
    add_text(s, k, Inches(0.95), yy, Inches(1.5),
             Inches(0.35), size=12, bold=True, color=GRAY)
    add_text(s, v, Inches(2.4), yy, Inches(4.2),
             Inches(0.35), size=12, color=DARK)
    yy += Inches(0.5)

# Variant B
add_rect(s, Inches(6.95), Inches(2.1), Inches(6.0), Inches(4.9), NAVY)
add_rect(s, Inches(6.95), Inches(2.1), Inches(6.0), Inches(0.7), GOLD)
add_text(s, "ВАРІАНТ B  ·  ТІЛЬКИ %",
         Inches(7.15), Inches(2.27), Inches(5.6), Inches(0.5),
         size=13, bold=True, color=NAVY)
add_text(s, "35% rev share, без фіксу",
         Inches(7.15), Inches(3.0), Inches(5.6), Inches(0.8),
         size=22, bold=True, color=WHITE)
b_items = [
    ("Термін:", "6 місяців"),
    ("Гарантія:", "$10K/міс до 90-го дня"),
    ("Якщо ні:", "Повертаю всі витрати"),
    ("Ризик:", "100% на мені"),
    ("Підходить, якщо:", "Не хочете платити фікс"),
]
yy = Inches(3.95)
for k, v in b_items:
    add_text(s, k, Inches(7.2), yy, Inches(1.7),
             Inches(0.35), size=12, bold=True, color=GOLD)
    add_text(s, v, Inches(8.9), yy, Inches(4.0),
             Inches(0.35), size=12, color=WHITE)
    yy += Inches(0.5)

# ============ SLIDE 9: NEXT STEPS ============
s = prs.slides.add_slide(BLANK)
add_bg(s)
header(s, "Наступні кроки", "Як стартуємо")

steps = [
    ("1", "Сьогодні", "Рішення про формат співпраці (A або B)"),
    ("2", "Завтра", "Підписуємо договір + бриф"),
    ("3", "День 3-5", "Запуск роботи: біо, Taplink, Telegram, бот"),
    ("4", "Тиждень 2", "Перші Reels у новій стратегії"),
    ("5", "Тиждень 4", "Запуск автоворонки + міні-курс"),
    ("6", "Тиждень 7", "Старт прогріву 12-го потоку"),
    ("7", "Тиждень 10", "Запуск курсу — ціль $25-35K"),
]
y = Inches(2.1)
for num, when, what in steps:
    add_rect(s, Inches(0.7), y, Inches(0.7), Inches(0.55), NAVY)
    add_text(s, num, Inches(0.7), y + Inches(0.05), Inches(0.7),
             Inches(0.45), size=18, bold=True, color=GOLD,
             align=PP_ALIGN.CENTER)
    add_text(s, when, Inches(1.6), y + Inches(0.07),
             Inches(2.4), Inches(0.4), size=14, bold=True, color=GOLD)
    add_text(s, what, Inches(4.1), y + Inches(0.07),
             Inches(9.0), Inches(0.4), size=14, color=DARK)
    y += Inches(0.65)

# ============ SLIDE 10: CTA ============
s = prs.slides.add_slide(BLANK)
add_bg(s, NAVY)
add_rect(s, 0, Inches(0), SW, Inches(0.3), GOLD)

add_text(s, "Алевтіно, у вас є все.",
         Inches(0.7), Inches(1.3), Inches(12), Inches(1.0),
         size=44, bold=True, color=WHITE)
add_text(s, "Я допоможу зібрати це у систему,",
         Inches(0.7), Inches(2.4), Inches(12), Inches(0.9),
         size=28, color=WHITE)
add_text(s, "яка приноситиме x5 уже за 90 днів.",
         Inches(0.7), Inches(3.05), Inches(12), Inches(0.9),
         size=28, bold=True, color=GOLD)

add_rect(s, Inches(0.7), Inches(4.7), Inches(12), Inches(0.05), GOLD)

add_text(s, "Що вам потрібно, щоб прийняти рішення сьогодні?",
         Inches(0.7), Inches(5.0), Inches(12), Inches(0.7),
         size=22, bold=True, color=WHITE)

add_text(s, "[Ім'я продюсера]   ·   [Telegram]   ·   [Email]",
         Inches(0.7), Inches(6.6), Inches(12), Inches(0.5),
         size=14, color=GOLD)

prs.save("/home/user/ethbtc-etf-bot/presentation/Alevtina_Drigant_Proposal.pptx")
print("PPTX saved")
