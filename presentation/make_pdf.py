from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                Table, TableStyle, PageBreak, KeepTogether)

NAVY = HexColor("#0B1F3A")
GOLD = HexColor("#C8A25B")
LIGHT = HexColor("#F5F1EA")
DARK = HexColor("#1A1A1A")
GRAY = HexColor("#6B6B6B")
WHITE = HexColor("#FFFFFF")
GREEN = HexColor("#2E8B57")

doc = SimpleDocTemplate(
    "/home/user/ethbtc-etf-bot/presentation/Alevtina_Drigant_Brief.pdf",
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
    title="Producer Proposal — Alevtina Drigant",
)

styles = getSampleStyleSheet()

H1 = ParagraphStyle('H1', parent=styles['Heading1'],
                    fontName='Helvetica-Bold', fontSize=22,
                    textColor=NAVY, spaceAfter=6, leading=26)
H2 = ParagraphStyle('H2', parent=styles['Heading2'],
                    fontName='Helvetica-Bold', fontSize=15,
                    textColor=NAVY, spaceBefore=14, spaceAfter=6,
                    leading=18)
H3 = ParagraphStyle('H3', parent=styles['Heading3'],
                    fontName='Helvetica-Bold', fontSize=12,
                    textColor=GOLD, spaceBefore=10, spaceAfter=4)
BODY = ParagraphStyle('BODY', parent=styles['BodyText'],
                      fontName='Helvetica', fontSize=10.5,
                      textColor=DARK, leading=15, alignment=TA_JUSTIFY,
                      spaceAfter=6)
BULLET = ParagraphStyle('BULLET', parent=BODY, leftIndent=14,
                        bulletIndent=2, spaceAfter=2)
KICKER = ParagraphStyle('KICKER', parent=styles['Normal'],
                        fontName='Helvetica-Bold', fontSize=9,
                        textColor=GOLD, spaceAfter=2)
SMALL = ParagraphStyle('SMALL', parent=styles['Normal'],
                       fontName='Helvetica', fontSize=9,
                       textColor=GRAY, leading=12)

story = []

# COVER
story.append(Paragraph("PRODUCER PROPOSAL", KICKER))
story.append(Paragraph("Алевтіна Дрігант", H1))
story.append(Paragraph(
    "Система масштабування курсу «Мистецтво говорити»", H2))
story.append(Paragraph(
    "<b>Ціль:</b> вийти з $3-5K за потік на $25-35K за потік "
    "та $150-250K/рік за 90 днів.", BODY))
story.append(Spacer(1, 6))

# Snapshot table
snap = [
    ["Метрика", "Зараз", "Через 90 днів"],
    ["Дохід з потоку курсу", "$3 000 – 5 000", "$25 000 – 35 000"],
    ["Канали продажу", "Тільки Instagram DM", "IG + Telegram + бот + лендінг"],
    ["База, що належить вам", "0", "2 000+ контактів"],
    ["Продуктів у лінійці", "1 (live-курс)", "5 (міні / live / premium / ретрит / B2B)"],
    ["Час експерта на тиждень", "хаотично", "5-7 годин"],
]
t = Table(snap, colWidths=[5.2*cm, 5*cm, 6.5*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT, WHITE]),
    ('GRID', (0,0), (-1,-1), 0.3, GRAY),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(t)

# 1. Diagnosis
story.append(Paragraph("1. Діагностика: 3 діри в грошах", H2))

story.append(Paragraph("Діра №1 — Продажі через DM", H3))
story.append(Paragraph(
    "Під продаючими постами 15+ коментарів «яка вартість?», «хочу деталі». "
    "Це люди з картками в руках. Але вони відправляються у DM. "
    "70-80% таких людей НЕ напишуть першими — стесняються, відволікаються, "
    "забувають. <b>Втрата ~$4 500 з кожного продаючого поста</b>.", BODY))

story.append(Paragraph("Діра №2 — Немає бази", H3))
story.append(Paragraph(
    "Instagram показує пости 5-10% підписників. З 12K вас бачать 600-1 200 "
    "людей. Немає Telegram-каналу, немає email-бази. Кожен запуск курсу "
    "починається з нуля.", BODY))

story.append(Paragraph("Діра №3 — Один продукт = один рівень доходу", H3))
story.append(Paragraph(
    "Зараз єдине джерело — live-курс «Мистецтво говорити». Між потоками "
    "тиша. Немає продуктів, які продаються щодня без вашої участі.", BODY))

# 2. Solution
story.append(Paragraph("2. Рішення: 90 днів до запуску x5", H2))

stages = [
    ("ЕТАП 1 · Тижні 1-3 · ФУНДАМЕНТ",
     ["Переупаковка біо + Taplink з оффером і ціною",
      "Telegram-канал + автоматизований бот",
      "Лід-магніт PDF «7 помилок мовлення»",
      "Хайлайти ВІДГУКИ / КУРС / ГАЙД",
      "Збір 15-20 відео-відгуків учениць"]),
    ("ЕТАП 2 · Тижні 4-6 · ВОРОНКА",
     ["Автоворонка в Telegram-боті (7-денна серія прогріву)",
      "Міні-курс у записі $97-147 — продажі на автопілоті",
      "Reels-стратегія: 5 відео/тиждень з готовими хуками",
      "Сторінка продажу курсу з 3-тарифною сіткою"]),
    ("ЕТАП 3 · Тижні 7-12 · ЗАПУСК",
     ["14-денний прогрів через всі канали до старту продажів",
      "Запуск 12-го потоку: ціль 50-60 учнів",
      "Premium-група $1 500 — 8-10 місць",
      "Перші переговори про корпоративні тренінги"]),
]
for title, items in stages:
    story.append(Paragraph(title, H3))
    for it in items:
        story.append(Paragraph("•&nbsp;&nbsp;" + it, BULLET))

# 3. Math
story.append(PageBreak())
story.append(Paragraph("3. Математика 12-го потоку", H2))

math_table = [
    ["", "ЗАРАЗ", "ПІСЛЯ СИСТЕМИ"],
    ["Охват аудиторії", "~800 (5-7%)", "~5 000 (IG + TG + Reels трафік)"],
    ["Заявок на курс", "15-20", "80-120"],
    ["Конверсія в оплату", "~50%", "~50%"],
    ["Учнів куплено", "10-15", "50-60"],
    ["Базовий чек", "$300", "$297 / $497 / $1 500"],
    ["Дохід з потоку", "$3 000 – $5 000", "$25 000 – $35 000"],
]
t = Table(math_table, colWidths=[5*cm, 5.5*cm, 6.2*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT, WHITE]),
    ('BACKGROUND', (2,-1), (2,-1), GOLD),
    ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ('GRID', (0,0), (-1,-1), 0.3, GRAY),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(t)
story.append(Spacer(1, 10))
story.append(Paragraph(
    "<b>Висновок:</b> один запуск з системою приносить більше, ніж зараз "
    "6 потоків. І це <b>без</b> урахування міні-курсу, корпоративів і ретритів.",
    BODY))

# 4. Annual forecast
story.append(Paragraph("4. Прогноз на 12 місяців", H2))

year = [
    ["Період", "Активність", "Дохід"],
    ["Місяці 1-2", "Підготовка системи", "$0"],
    ["Місяць 3", "Запуск 12-го потоку", "$25-35K"],
    ["Місяці 4-5", "Автопродажі + корпоративи", "$10-16K"],
    ["Місяць 6", "Запуск 13-го потоку", "$30-45K"],
    ["Місяць 7", "Літній ретрит у Європі", "$15-25K"],
    ["Місяці 8-9", "Автопродажі + корпоративи", "$14-24K"],
    ["Місяць 10", "Запуск 14-го потоку", "$35-50K"],
    ["Місяці 11-12", "Новорічний запуск + автопродажі", "$15-25K"],
    ["РАЗОМ ЗА РІК", "Зростання x3 – x5 від поточного", "$150-250K"],
]
t = Table(year, colWidths=[3.8*cm, 8.5*cm, 4.4*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-2), [LIGHT, WHITE]),
    ('BACKGROUND', (0,-1), (-1,-1), GOLD),
    ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ('TEXTCOLOR', (0,-1), (-1,-1), NAVY),
    ('GRID', (0,0), (-1,-1), 0.3, GRAY),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(t)

# 5. Roles
story.append(Paragraph("5. Розподіл ролей", H2))

roles = [
    ["АЛЕВТІНА (експерт + обличчя)", "ПРОДЮСЕР (система + продажі)"],
    ["Записує Reels (5/тиждень)", "Воронка, бот, Telegram, Taplink"],
    ["Веде ефіри і live-уроки курсу", "Контент-стратегія + монтаж"],
    ["Дає експертну глибину контенту", "Запуски курсу під ключ"],
    ["Спілкується з преміум-учнями", "Аналітика, дашборди, тести"],
    ["Час: 5-7 годин/тиждень", "Перемовини B2B + корпоративи"],
]
t = Table(roles, colWidths=[8.35*cm, 8.35*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,0), LIGHT),
    ('BACKGROUND', (1,0), (1,0), NAVY),
    ('TEXTCOLOR', (1,0), (1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ('GRID', (0,0), (-1,-1), 0.3, GRAY),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(t)

# 6. Offer
story.append(PageBreak())
story.append(Paragraph("6. Оффер співпраці", H2))

story.append(Paragraph("Варіант A — Рекомендований", H3))
story.append(Paragraph(
    "<b>$1 000/міс фікс  +  20% від нового доходу</b>", BODY))
a = [
    ["Термін", "3 місяці пілот, далі продовження за результатом"],
    ["KPI 1", "Запуск 12-го потоку на $25 000+"],
    ["KPI 2", "Telegram-база 2 000+ підписників"],
    ["KPI 3", "Автопродажі міні-курсу $5 000/міс до 90-го дня"],
    ["Ризик", "Розділений 50/50 — фікс покриває операційку"],
]
t = Table(a, colWidths=[3.5*cm, 13.2*cm])
t.setStyle(TableStyle([
    ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ('TEXTCOLOR', (0,0), (0,-1), GOLD),
    ('ROWBACKGROUNDS', (0,0), (-1,-1), [LIGHT, WHITE]),
    ('GRID', (0,0), (-1,-1), 0.3, GRAY),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(t)

story.append(Paragraph("Варіант B — Тільки %", H3))
story.append(Paragraph(
    "<b>35% від нового доходу, без фіксу</b>", BODY))
b = [
    ["Термін", "6 місяців"],
    ["Гарантія", "$10 000/міс до 90-го дня"],
    ["Якщо ні", "Повертаю всі понесені витрати"],
    ["Ризик", "100% на продюсері"],
    ["Кому підходить", "Якщо не хочете платити фікс наперед"],
]
t = Table(b, colWidths=[3.5*cm, 13.2*cm])
t.setStyle(TableStyle([
    ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ('TEXTCOLOR', (0,0), (0,-1), GOLD),
    ('ROWBACKGROUNDS', (0,0), (-1,-1), [LIGHT, WHITE]),
    ('GRID', (0,0), (-1,-1), 0.3, GRAY),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(t)

# 7. Next steps
story.append(Paragraph("7. Наступні кроки", H2))
steps = [
    ("Сьогодні", "Рішення про формат співпраці (A або B)"),
    ("Завтра", "Підписуємо договір + бриф + доступи"),
    ("День 3-5", "Запуск роботи: біо, Taplink, Telegram, бот"),
    ("Тиждень 2", "Перші Reels у новій стратегії"),
    ("Тиждень 4", "Запуск автоворонки + міні-курс у записі"),
    ("Тиждень 7", "Старт 14-денного прогріву до 12-го потоку"),
    ("Тиждень 10", "Запуск курсу — ціль $25-35K"),
]
data = [["#", "Коли", "Що робимо"]]
for i, (when, what) in enumerate(steps, 1):
    data.append([str(i), when, what])
t = Table(data, colWidths=[1*cm, 3.5*cm, 12.2*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), NAVY),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (1,1), (1,-1), 'Helvetica-Bold'),
    ('TEXTCOLOR', (1,1), (1,-1), GOLD),
    ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT, WHITE]),
    ('GRID', (0,0), (-1,-1), 0.3, GRAY),
    ('ALIGN', (0,0), (0,-1), 'CENTER'),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(t)

# CTA
story.append(Spacer(1, 18))
cta = Table([[
    Paragraph(
        "<font color='white'><b>Алевтіно, у вас є все.</b><br/>"
        "Я допоможу зібрати це у систему,<br/>"
        "<font color='#C8A25B'><b>яка приноситиме x5 уже за 90 днів.</b></font>"
        "</font>",
        ParagraphStyle('cta', fontName='Helvetica', fontSize=13,
                       leading=20, alignment=TA_CENTER))
]], colWidths=[16.7*cm])
cta.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), NAVY),
    ('TOPPADDING', (0,0), (-1,-1), 18),
    ('BOTTOMPADDING', (0,0), (-1,-1), 18),
    ('LEFTPADDING', (0,0), (-1,-1), 20),
    ('RIGHTPADDING', (0,0), (-1,-1), 20),
]))
story.append(cta)

story.append(Spacer(1, 8))
story.append(Paragraph(
    "Контакти продюсера:&nbsp;&nbsp;[Ім'я]&nbsp;·&nbsp;[Telegram]&nbsp;·&nbsp;[Email]",
    SMALL))

doc.build(story)
print("PDF saved")
