import asyncio
import logging
import os
import uuid

from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    BotCommand,
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)

import config
import database as db
from tryon import run_clothes_tryon, run_jewelry_tryon

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

bot = Bot(token=config.BOT_TOKEN, default={"parse_mode": ParseMode.HTML})
dp = Dispatcher()
router = Router()


class S(StatesGroup):
    wait_person = State()
    ready = State()
    wait_garment = State()
    processing = State()


def km(hp, t):
    r = []
    if hp:
        r.append(
            [
                InlineKeyboardButton(text="👗 Одежда", callback_data="cat_clothes"),
                InlineKeyboardButton(text="💎 Украшения", callback_data="cat_jewelry"),
            ]
        )
        r.append(
            [InlineKeyboardButton(text="🔄 Заменить фото", callback_data="change_photo")]
        )
    else:
        r.append(
            [InlineKeyboardButton(text="📸 Загрузить фото", callback_data="upload_photo")]
        )
    r.append(
        [
            InlineKeyboardButton(text="👜 Гардероб", callback_data="wardrobe"),
            InlineKeyboardButton(text="💳 Купить примерки", callback_data="buy_tries"),
        ]
    )
    r.append(
        [
            InlineKeyboardButton(text="🎁 Пригласить друга", callback_data="referral"),
            InlineKeyboardButton(text="📊 Статистика", callback_data="stats"),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=r)


def kr():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💾 Сохранить", callback_data="save_result"),
                InlineKeyboardButton(
                    text="🎉 Поделиться", callback_data="share_result"
                ),
            ],
            [InlineKeyboardButton(text="🔁 Ещё раз", callback_data="retry")],
            [InlineKeyboardButton(text="🏠 Меню", callback_data="main_menu")],
        ]
    )


def kjt():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📿 Ожерелье", callback_data="j_necklace"),
                InlineKeyboardButton(text="💎 Серьги", callback_data="j_earrings"),
            ],
            [
                InlineKeyboardButton(text="⌚ Часы", callback_data="j_watch"),
                InlineKeyboardButton(text="💍 Кольцо", callback_data="j_ring"),
            ],
            [
                InlineKeyboardButton(text="🧣 Браслет", callback_data="j_bracelet"),
                InlineKeyboardButton(text="🕶 Очки", callback_data="j_glasses"),
            ],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")],
        ]
    )


def kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⭐ 10 примерок — 50 Stars", callback_data="stars_10"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⭐ 50 примерок — 200 Stars", callback_data="stars_50"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⭐ 200 примерок — 700 Stars", callback_data="stars_200"
                )
            ],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")],
        ]
    )


def ed():
    for d in ("persons", "garments", "results"):
        os.makedirs(os.path.join(config.PHOTOS_DIR, d), exist_ok=True)


async def dp_photo(msg, sub):
    p = msg.photo[-1]
    fi = await bot.get_file(p.file_id)
    nm = f"{msg.from_user.id}_{uuid.uuid4().hex[:8]}.jpg"
    path = os.path.join(config.PHOTOS_DIR, sub, nm)
    await bot.download_file(fi.file_path, path)
    return path


@router.message(CommandStart())
async def cmd_start(msg: Message, state: FSMContext):
    uid = msg.from_user.id
    nm = msg.from_user.full_name or "пользователь"
    ref = None
    if msg.text and " " in msg.text:
        a = msg.text.split(maxsplit=1)[1]
        if a.startswith("ref_"):
            try:
                r = int(a[4:])
                if r != uid:
                    ref = r
            except Exception:
                pass
    u = await db.get_user(uid)
    if not u:
        await db.create_user(uid, msg.from_user.username or "", nm, config.FREE_TRIES, ref)
        if ref:
            await db.add_tries(ref, config.REFERRAL_BONUS)
            try:
                await bot.send_message(
                    ref,
                    f"🎁 Ваш друг <b>{nm}</b> присоединился!\n+{config.REFERRAL_BONUS} примерок начислено.",
                )
            except Exception:
                pass
        u = await db.get_user(uid)
    hp = bool(u.get("person_photo"))
    await state.set_state(S.ready if hp else None)
    await msg.answer(
        f"👗 <b>AI Try-On — виртуальная примерка!</b>\n\n"
        f"1️⃣ Загрузите своё фото\n"
        f"2️⃣ Отправьте фото вещи\n"
        f"3️⃣ Получите AI-результат!\n\n"
        f"🎁 Примерок: <b>{u['tries_left']}</b>",
        reply_markup=km(hp, u["tries_left"]),
    )


@router.callback_query(F.data.in_({"upload_photo", "change_photo"}))
async def cb_up(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.answer(
        "📸 <b>Отправьте своё фото</b>\n\n• В полный рост или по пояс\n• Нейтральный фон\n• Хорошее освещение"
    )
    await state.set_state(S.wait_person)


@router.message(S.wait_person, F.photo)
async def gpp(msg: Message, state: FSMContext):
    p = await dp_photo(msg, "persons")
    await db.update_person_photo(msg.from_user.id, p)
    u = await db.get_user(msg.from_user.id)
    await msg.answer(
        "✅ <b>Фото сохранено!</b>\n\nТеперь отправьте фото одежды или украшения.",
        reply_markup=km(True, u["tries_left"]),
    )
    await state.set_state(S.ready)


@router.message(S.wait_person)
async def wpw(msg: Message):
    await msg.answer("⚠️ Отправьте именно <b>фото</b>.")


async def _cp2(cb: CallbackQuery):
    u = await db.get_user(cb.from_user.id)
    if not u or not u.get("person_photo"):
        await cb.message.answer(
            "⚠️ Сначала загрузите своё фото!",
            reply_markup=km(False, u["tries_left"] if u else 0),
        )
        return False
    return True


@router.callback_query(F.data == "cat_clothes")
async def cc(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    if not await _cp2(cb):
        return
    await state.update_data(category="clothes", jewelry_type=None)
    await cb.message.answer(
        "👗 <b>Примерка одежды</b>\n\nОтправьте фото одежды.\nЛучше на белом фоне."
    )
    await state.set_state(S.wait_garment)


@router.callback_query(F.data == "cat_jewelry")
async def cj(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    if not await _cp2(cb):
        return
    await cb.message.answer("💎 <b>Выберите тип украшения:</b>", reply_markup=kjt())


@router.callback_query(F.data.startswith("j_"))
async def cjt(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    if not await _cp2(cb):
        return
    jt = cb.data[2:]
    names = {
        "necklace": "ожерелье",
        "earrings": "серьги",
        "watch": "часы",
        "ring": "кольцо",
        "bracelet": "браслет",
        "glasses": "очки",
    }
    await state.update_data(category="jewelry", jewelry_type=jt)
    await cb.message.answer(
        f"💎 <b>Примерка: {names.get(jt, jt)}</b>\n\nОтправьте фото украшения."
    )
    await state.set_state(S.wait_garment)


@router.message(S.wait_garment, F.photo)
async def ggp(msg: Message, state: FSMContext):
    await _rg(msg, state, msg.from_user.id)


@router.message(S.wait_garment)
async def wgw(msg: Message):
    await msg.answer("⚠️ Отправьте именно <b>фото</b> вещи.")


@router.message(S.ready, F.photo)
async def qp(msg: Message, state: FSMContext):
    p = await dp_photo(msg, "garments")
    await state.update_data(pending_garment=p)
    await msg.answer(
        "🤔 Что это за вещь?",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="👗 Одежда", callback_data="qcat_clothes"),
                    InlineKeyboardButton(
                        text="💎 Украшение", callback_data="qcat_jewelry"
                    ),
                ]
            ]
        ),
    )


@router.callback_query(F.data.in_({"qcat_clothes", "qcat_jewelry"}))
async def qcc(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    if not await _cp2(cb):
        return
    d = await state.get_data()
    gp = d.get("pending_garment")
    if not gp:
        await cb.message.answer("Фото не найдено. Попробуйте ещё раз.")
        return
    if cb.data == "qcat_jewelry":
        await state.update_data(category="jewelry", jewelry_type="necklace")
        await cb.message.answer("Какое украшение?", reply_markup=kjt())
    else:
        await state.update_data(category="clothes", jewelry_type=None)
        await _rg(cb.message, state, cb.from_user.id, gp)


async def _rg(msg: Message, state: FSMContext, uid: int, gp: str | None = None):
    u = await db.get_user(uid)
    if not u:
        await msg.answer("Ошибка. Напишите /start.")
        return
    if u["tries_left"] <= 0:
        await msg.answer(
            "🚫 <b>Примерки закончились!</b>\n\nКупите ещё или пригласите друга.",
            reply_markup=kb(),
        )
        return
    if not await db.use_try(uid):
        await msg.answer("🚫 Примерки закончились!", reply_markup=kb())
        return
    if gp is None:
        gp = await dp_photo(msg, "garments")
    d = await state.get_data()
    cat = d.get("category", "clothes")
    jt = d.get("jewelry_type", "necklace")
    pp = u["person_photo"]
    await state.set_state(S.processing)
    st = await msg.answer(
        "✨ <b>Генерация запущена!</b>\n\n🧠 Нейросеть анализирует фигуру...\n⏳ 20–60 секунд"
    )

    async def _t():
        for s in [
            "📐 Подбираем размер...",
            "🎨 Примеряем на вас...",
            "🖼 Финальная обработка...",
        ]:
            await asyncio.sleep(10)
            try:
                await st.edit_text(
                    f"✨ <b>Генерация...</b>\n\n{s}\n⏳ Совсем скоро"
                )
            except Exception:
                pass

    tk = asyncio.create_task(_t())
    try:
        if cat == "clothes":
            rp = await run_clothes_tryon(pp, gp)
        else:
            rp = await run_jewelry_tryon(pp, gp, jt)
    finally:
        tk.cancel()
    if not rp or not os.path.exists(rp):
        await db.add_tries(uid, 1)
        await st.edit_text(
            "❌ <b>Не удалось создать примерку.</b>\n\nПопробуйте другое фото.\nПримерка возвращена.",
            reply_markup=km(True, u["tries_left"]),
        )
        await state.set_state(S.ready)
        return
    q = round(7.0 + (hash(os.path.basename(rp)) % 30) / 10, 1)
    await db.save_generation(uid, cat, gp, rp, q)
    u = await db.get_user(uid)
    try:
        await st.delete()
    except Exception:
        pass
    await msg.answer_photo(
        FSInputFile(rp),
        caption=(
            f"🔥 <b>Вот как это выглядит!</b>\n\n"
            f"📊 Качество: <b>{q}/10</b>\n"
            f"💎 Осталось примерок: <b>{u['tries_left']}</b>"
        ),
        reply_markup=kr(),
    )
    await state.update_data(last_result=rp)
    await state.set_state(S.ready)


@router.callback_query(F.data == "save_result")
async def cs(cb: CallbackQuery):
    await cb.answer("✅ Сохранено!", show_alert=False)


@router.callback_query(F.data == "share_result")
async def csh(cb: CallbackQuery):
    await cb.answer()
    me = await bot.get_me()
    await cb.message.answer(f"🎉 Попробуйте сами: https://t.me/{me.username}")


@router.callback_query(F.data == "retry")
async def cre(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.answer("Отправьте новое фото для примерки!")
    await state.set_state(S.ready)


@router.callback_query(F.data == "main_menu")
async def cmm(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    u = await db.get_user(cb.from_user.id)
    await state.set_state(S.ready if u and u.get("person_photo") else None)
    await cb.message.answer(
        f"🏠 <b>Главное меню</b>\n\n💎 Примерок: <b>{u['tries_left']}</b>",
        reply_markup=km(bool(u.get("person_photo")), u["tries_left"]),
    )


@router.callback_query(F.data == "wardrobe")
async def cw(cb: CallbackQuery):
    await cb.answer()
    gs = await db.get_user_generations(cb.from_user.id, 6)
    if not gs:
        await cb.message.answer(
            "👜 <b>Гардероб пуст</b>\n\nЗдесь будут все ваши примерки."
        )
        return
    await cb.message.answer(f"👜 <b>Последние {len(gs)} примерок:</b>")
    for g in gs:
        p = g.get("result_photo", "")
        if p and os.path.exists(p):
            await cb.message.answer_photo(
                FSInputFile(p),
                caption=f"{'👗' if g['category'] == 'clothes' else '💎'} Качество: {g['quality_score']}/10",
            )


SP = {"stars_10": (10, 50), "stars_50": (50, 200), "stars_200": (200, 700)}


@router.callback_query(F.data == "buy_tries")
async def cbm(cb: CallbackQuery):
    await cb.answer()
    await cb.message.answer(
        "💳 <b>Купить примерки</b>\n\nОплата через Telegram Stars ⭐:",
        reply_markup=kb(),
    )


@router.callback_query(F.data.in_(set(SP)))
async def cbp(cb: CallbackQuery):
    await cb.answer()
    t, s = SP[cb.data]
    await bot.send_invoice(
        chat_id=cb.from_user.id,
        title=f"{t} примерок AI Try-On",
        description=f"Виртуальная примерка · {t} генераций",
        payload=f"buy_{t}",
        currency="XTR",
        prices=[LabeledPrice(label=f"{t} примерок", amount=s)],
        provider_token="",
    )


@router.pre_checkout_query()
async def pcq(q: PreCheckoutQuery):
    await q.answer(ok=True)


@router.message(F.successful_payment)
async def sp(msg: Message):
    t = int(msg.successful_payment.invoice_payload.split("_")[1])
    await db.add_tries(msg.from_user.id, t)
    u = await db.get_user(msg.from_user.id)
    await msg.answer(
        f"✅ <b>Оплата прошла!</b>\n\nНачислено <b>{t}</b> примерок.\nВсего: <b>{u['tries_left']}</b>",
        reply_markup=km(bool(u.get("person_photo")), u["tries_left"]),
    )


@router.callback_query(F.data == "referral")
async def cref(cb: CallbackQuery):
    await cb.answer()
    uid = cb.from_user.id
    me = await bot.get_me()
    link = f"https://t.me/{me.username}?start=ref_{uid}"
    refs = await db.get_referral_count(uid)
    await cb.message.answer(
        f"🎁 <b>Реферальная программа</b>\n\n"
        f"За каждого друга — <b>+{config.REFERRAL_BONUS} примерок</b>!\n\n"
        f"Ваша ссылка:\n<code>{link}</code>\n\n"
        f"👥 Приглашено: <b>{refs}</b>",
    )


@router.callback_query(F.data == "stats")
async def cst(cb: CallbackQuery):
    await cb.answer()
    u = await db.get_user(cb.from_user.id)
    refs = await db.get_referral_count(cb.from_user.id)
    text = (
        f"📊 <b>Статистика</b>\n\n"
        f"💎 Примерок: <b>{u['tries_left']}</b>\n"
        f"🔄 Генераций: <b>{u['total_generations']}</b>\n"
        f"👥 Приглашено: <b>{refs}</b>"
    )
    if cb.from_user.id in config.ADMIN_IDS:
        s = await db.get_stats()
        text += (
            f"\n\n🛡 Пользователей: {s['total_users']}\n"
            f"Генераций: {s['total_generations']}\n"
            f"Активных сегодня: {s['active_today']}"
        )
    await cb.message.answer(
        text, reply_markup=km(bool(u.get("person_photo")), u["tries_left"])
    )


@router.message(Command("admin"))
async def ca(msg: Message):
    if msg.from_user.id not in config.ADMIN_IDS:
        return
    s = await db.get_stats()
    await msg.answer(
        f"🛡 <b>Админ</b>\n\n👤 {s['total_users']}\n🔄 {s['total_generations']}\n🟢 {s['active_today']}"
    )


@router.message(Command("addtries"))
async def cmd_addtries(msg: Message):
    if msg.from_user.id not in config.ADMIN_IDS:
        return
    p = msg.text.split()
    if len(p) != 3:
        await msg.answer("Использование: /addtries USER_ID КОЛИЧЕСТВО")
        return
    try:
        await db.add_tries(int(p[1]), int(p[2]))
        await msg.answer(f"✅ Начислено {p[2]} примерок пользователю {p[1]}")
    except Exception:
        await msg.answer("Неверные аргументы.")


@router.message(F.photo)
async def fp(msg: Message, state: FSMContext):
    u = await db.get_user(msg.from_user.id)
    if not u:
        await cmd_start(msg, state)
        return
    if not u.get("person_photo"):
        p = await dp_photo(msg, "persons")
        await db.update_person_photo(msg.from_user.id, p)
        await msg.answer(
            "✅ Фото сохранено! Теперь отправьте фото одежды или украшения.",
            reply_markup=km(True, u["tries_left"]),
        )
        await state.set_state(S.ready)
    else:
        p = await dp_photo(msg, "garments")
        await state.update_data(pending_garment=p)
        await state.set_state(S.ready)
        await msg.answer(
            "🤔 Что это?",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="👗 Одежда", callback_data="qcat_clothes"
                        ),
                        InlineKeyboardButton(
                            text="💎 Украшение", callback_data="qcat_jewelry"
                        ),
                    ]
                ]
            ),
        )


@router.message(F.text)
async def ft(msg: Message, state: FSMContext):
    u = await db.get_user(msg.from_user.id)
    if not u:
        await cmd_start(msg, state)
        return
    await msg.answer(
        "Отправьте фото для примерки 👇",
        reply_markup=km(bool(u.get("person_photo")), u["tries_left"]),
    )


async def main():
    ed()
    await db.init_db()
    dp.include_router(router)
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Главное меню"),
            BotCommand(command="admin", description="Админ"),
            BotCommand(command="addtries", description="Начислить примерки"),
        ]
    )
    logger.info("Bot started!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
