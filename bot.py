import re
import asyncio
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN, ADMIN_IDS, ASSETS_WELCOME_PATH, REG_CSV_PATH
from keyboards import (
    CTA_JOIN_TEXT,
    BTN_MY_INFO,
    BTN_HELP,
<<<<<<< HEAD
    BTN_ADMIN_LIST,
    BTN_ADMIN_EXPORT,
    kb_welcome,
    kb_after_registered,
    kb_after_registered_admin,
=======
    kb_welcome,
    kb_after_registered,
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
    kb_contact_share,
    kb_regions,
    kb_remove,
    REGIONS,
)
import storage

STATE_NAME, STATE_PHONE, STATE_REGION = range(3)

WELCOME_TEXT = (
    "Growz tomonidan qishloq xo'jaligi sohasida yaqin kunlarda maxsus uchrashuv va amaliy tadbirlar "
    "tashkil etilishi rejalashtirilmoqda.\n"
    "Ushbu tadbirlar:\n"
    "• fermerlar va eksportyorlar uchun\n"
    "• amaliy bilim va tajriba almashish uchun\n"
    "• yangi imkoniyatlar va hamkorliklar uchun mo‘ljallangan\n\n"
    "Hozirda qaysi hududlardan fermerlar qiziqish bildirayotganini aniqlayapmiz.\n"
    "Agar ishtirok etishni istasangiz, qisqa ma’lumot qoldiring."
)

CONFIRM_TEXT = (
    "Rahmat!\n"
    "Ma’lumotlaringiz qabul qilindi.\n"
    "Yaqin kunlarda Growz tomonidan tashkil etiladigan tadbirlar bo‘yicha siz bilan bog‘lanamiz."
)

LOCK = asyncio.Lock()

<<<<<<< HEAD

def _is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


def _kb_after_registered_for(user_id: int):
    return kb_after_registered_admin() if _is_admin(user_id) else kb_after_registered()


def _normalize_phone(phone: str) -> str:
    return re.sub(r"\D+", "", phone or "").strip()

=======
def _normalize_phone(phone: str) -> str:
    return (phone or "").strip()
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9

def _is_valid_full_name(text: str) -> bool:
    if not text:
        return False
    t = text.strip()
    parts = [p for p in re.split(r"\s+", t) if p]
    if len(parts) < 2:
        return False
    if len(t) < 5:
        return False
    return True

<<<<<<< HEAD

=======
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(ASSETS_WELCOME_PATH, "rb") as f:
            await update.message.reply_photo(photo=f)
    except Exception:
        pass

    await update.message.reply_text(WELCOME_TEXT, reply_markup=kb_welcome())

<<<<<<< HEAD

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    storage.ensure_storage()
    storage.migrate_old_csv_if_needed()
=======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    storage.ensure_storage()
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9

    tg_id = update.effective_user.id
    existing = storage.find_by_telegram_id(tg_id)

    if existing:
        await update.message.reply_text(
            "✅ Siz allaqachon ro‘yxatdan o‘tgansiz.\n\n"
            "Quyidagi tugmalar orqali ma’lumotlaringizni ko‘rishingiz mumkin.",
<<<<<<< HEAD
            reply_markup=_kb_after_registered_for(tg_id)
=======
            reply_markup=kb_after_registered()
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
        )
        return

    await send_welcome(update, context)

<<<<<<< HEAD

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    storage.ensure_storage()
    storage.migrate_old_csv_if_needed()

    tg_id = update.effective_user.id
    existing = storage.find_by_telegram_id(tg_id)

=======
async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    storage.ensure_storage()
    tg_id = update.effective_user.id

    existing = storage.find_by_telegram_id(tg_id)
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
    if existing:
        await update.message.reply_text(
            "✅ Siz allaqachon ro‘yxatdan o‘tgansiz.\n"
            "Qayta ro‘yxatdan o‘tish mumkin emas.\n\n"
            "📄 Ma’lumotlarim tugmasini bosing.",
<<<<<<< HEAD
            reply_markup=_kb_after_registered_for(tg_id)
=======
            reply_markup=kb_after_registered()
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "Iltimos, ism va familiyangizni kiriting.\n"
        "Masalan: Aliyev Sardor",
        reply_markup=kb_remove()
    )
    return STATE_NAME

<<<<<<< HEAD

=======
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    if not _is_valid_full_name(text):
        await update.message.reply_text(
            "❌ Ism va familiya 2 ta so‘zdan iborat bo‘lishi kerak.\n"
            "Masalan: Aliyev Sardor\n\n"
            "Qaytadan kiriting:"
        )
        return STATE_NAME

    context.user_data["full_name"] = text

    await update.message.reply_text(
        "Bog‘lanish va tadbir tafsilotlarini yetkazish uchun telefon raqamingizni yuboring.\n"
        "Pastdagi tugma orqali yuboring 👇",
        reply_markup=kb_contact_share()
    )
    return STATE_PHONE

<<<<<<< HEAD

=======
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.contact:
        await update.message.reply_text(
            "❌ Iltimos, telefon raqamingizni *faqat tugma orqali* yuboring 👇",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=kb_contact_share()
        )
        return STATE_PHONE

    contact = update.message.contact

    if contact.user_id and contact.user_id != update.effective_user.id:
        await update.message.reply_text(
            "❌ Iltimos, *o‘zingizning* telefon raqamingizni yuboring.\n"
            "Pastdagi tugma orqali yuboring 👇",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=kb_contact_share()
        )
        return STATE_PHONE

    phone = _normalize_phone(contact.phone_number)
    if not phone:
        await update.message.reply_text(
            "❌ Telefon raqam aniqlanmadi. Qaytadan yuboring 👇",
            reply_markup=kb_contact_share()
        )
        return STATE_PHONE

<<<<<<< HEAD
    # Эски ёзув бўлса (телефон бор, tg_id йўқ) — tg_id боғлаб қўямиз
    storage.bind_telegram_id_by_phone(update.effective_user.id, phone)

    used = storage.find_by_phone(phone)
    if used:
        if str(used.get("telegram_id", "")).strip() == str(update.effective_user.id):
            await update.message.reply_text(
                "✅ Siz allaqachon ro‘yxatdan o‘tgansiz.\n"
                "📄 Ma’lumotlarim tugmasini bosing.",
                reply_markup=_kb_after_registered_for(update.effective_user.id)
            )
        else:
            await update.message.reply_text(
                "❌ Ushbu telefon raqam bilan avval ro‘yxatdan o‘tilgan.\n"
                "Qayta ro‘yxatdan o‘tish mumkin emas.\n\n"
                "Agar bu xato bo‘lsa, admin bilan bog‘laning.",
                reply_markup=_kb_after_registered_for(update.effective_user.id)
            )
=======
    used = storage.find_by_phone(phone)
    if used:
        await update.message.reply_text(
            "❌ Ushbu telefon raqam bilan avval ro‘yxatdan o‘tilgan.\n"
            "Qayta ro‘yxatdan o‘tish mumkin emas.\n\n"
            "Agar bu xato bo‘lsa, admin bilan bog‘laning.",
            reply_markup=kb_after_registered()
        )
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
        return ConversationHandler.END

    context.user_data["phone"] = phone

    await update.message.reply_text(
        "Qaysi viloyatdan ishtirok etmoqchisiz?\n"
        "Quyidagi ro‘yxatdan tanlang 👇",
        reply_markup=kb_regions()
    )
    return STATE_REGION

<<<<<<< HEAD

=======
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
async def handle_region(update: Update, context: ContextTypes.DEFAULT_TYPE):
    region = (update.message.text or "").strip()

    if region not in REGIONS:
        await update.message.reply_text(
            "❌ Iltimos, viloyatni *faqat ro‘yxatdan* tanlang 👇",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=kb_regions()
        )
        return STATE_REGION

    full_name = context.user_data.get("full_name", "").strip()
    phone = context.user_data.get("phone", "").strip()
    tg_id = update.effective_user.id

    async with LOCK:
        try:
            storage.add_registration(
                telegram_id=tg_id,
                full_name=full_name,
                phone=phone,
                region=region
            )
        except ValueError as e:
            if str(e) == "already_registered_by_tg":
                await update.message.reply_text(
                    "✅ Siz allaqachon ro‘yxatdan o‘tgansiz.\n"
                    "Qayta ro‘yxatdan o‘tish mumkin emas.",
<<<<<<< HEAD
                    reply_markup=_kb_after_registered_for(tg_id)
=======
                    reply_markup=kb_after_registered()
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
                )
                return ConversationHandler.END
            if str(e) == "phone_already_used":
                await update.message.reply_text(
                    "❌ Ushbu telefon raqam bilan avval ro‘yxatdan o‘tilgan.\n"
                    "Qayta ro‘yxatdan o‘tish mumkin emas.",
<<<<<<< HEAD
                    reply_markup=_kb_after_registered_for(tg_id)
=======
                    reply_markup=kb_after_registered()
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
                )
                return ConversationHandler.END
            raise

<<<<<<< HEAD
    await update.message.reply_text(CONFIRM_TEXT, reply_markup=_kb_after_registered_for(tg_id))
    context.user_data.clear()
    return ConversationHandler.END


=======
    await update.message.reply_text(CONFIRM_TEXT, reply_markup=kb_after_registered())
    context.user_data.clear()
    return ConversationHandler.END

>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "✅ Bekor qilindi.\nQayta boshlash uchun /start bosing.",
        reply_markup=kb_welcome()
    )
    return ConversationHandler.END

<<<<<<< HEAD

async def my_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    storage.ensure_storage()
    storage.migrate_old_csv_if_needed()

    tg_id = update.effective_user.id
    existing = storage.find_by_telegram_id(tg_id)

=======
async def my_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id
    existing = storage.find_by_telegram_id(tg_id)
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
    if not existing:
        await update.message.reply_text(
            "Siz hali ro‘yxatdan o‘tmagansiz.\n/start bosing.",
            reply_markup=kb_welcome()
        )
        return

    msg = (
        "📄 *Sizning ma’lumotlaringiz:*\n"
        f"• Ism-familiya: *{existing.get('full_name','-')}*\n"
        f"• Telefon: *{existing.get('phone','-')}*\n"
        f"• Viloyat: *{existing.get('region','-')}*\n"
        f"• Sana: *{existing.get('registered_at','-')}*"
    )
<<<<<<< HEAD
    await update.message.reply_text(
        msg,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=_kb_after_registered_for(tg_id)
    )

=======
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=kb_after_registered())
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9

async def help_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Yordam:\n"
        "• Ro‘yxatdan o‘tish uchun /start yoki 👉 Ishtirok etmoqchiman tugmasi.\n"
        "• Jarayonni bekor qilish: /cancel\n"
        "• Ro‘yxatdan o‘tgan bo‘lsangiz, 📄 Ma’lumotlarim tugmasi orqali tekshiring.",
<<<<<<< HEAD
        reply_markup=_kb_after_registered_for(update.effective_user.id)
    )


async def export_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not _is_admin(user_id):
=======
        reply_markup=kb_after_registered()
    )

async def export_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
        await update.message.reply_text("❌ Sizda admin huquqi yo‘q.")
        return

    storage.ensure_storage()
<<<<<<< HEAD
    storage.migrate_old_csv_if_needed()

=======
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
    try:
        with open(REG_CSV_PATH, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename="registrations.csv",
                caption="✅ Registrations CSV (Excel’da ham ochiladi)."
            )
    except Exception as e:
        await update.message.reply_text(f"❌ Export xato: {e}")

<<<<<<< HEAD

async def admin_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not _is_admin(user_id):
        await update.message.reply_text("❌ Sizda admin huquqi yo‘q.")
        return

    storage.ensure_storage()
    storage.migrate_old_csv_if_needed()

    rows = storage.list_last(limit=20)
    if not rows:
        await update.message.reply_text("Hozircha ro‘yxat bo‘sh.")
        return

    text = "📋 *Oxirgi 20 ta ro‘yxatdan o‘tganlar:*\n\n"
    for i, r in enumerate(rows, start=1):
        text += (
            f"{i}) *{r.get('full_name','-')}*\n"
            f"   📞 {r.get('phone','-')}\n"
            f"   📍 {r.get('region','-')}\n"
            f"   🕒 {r.get('registered_at','-')}\n\n"
        )

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=_kb_after_registered_for(user_id)
    )


async def admin_export_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await export_csv(update, context)


async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    storage.ensure_storage()
    storage.migrate_old_csv_if_needed()

=======
async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
    tg_id = update.effective_user.id
    existing = storage.find_by_telegram_id(tg_id)

    if existing:
        await update.message.reply_text(
            "✅ Siz allaqachon ro‘yxatdan o‘tgansiz.\n"
            "📄 Ma’lumotlarim tugmasini bosing yoki /start yuboring.",
<<<<<<< HEAD
            reply_markup=_kb_after_registered_for(tg_id)
=======
            reply_markup=kb_after_registered()
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
        )
    else:
        await update.message.reply_text(
            "Ro‘yxatdan o‘tish uchun /start bosing yoki 👉 Ishtirok etmoqchiman tugmasini bosing.",
            reply_markup=kb_welcome()
        )

<<<<<<< HEAD

=======
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
def build_application():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN topilmadi. .env faylni tekshiring.")

    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex(f"^{re.escape(CTA_JOIN_TEXT)}$"), join),
            CommandHandler("start", start),
        ],
        states={
            STATE_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name),
            ],
            STATE_PHONE: [
                MessageHandler(filters.CONTACT, handle_phone),
                MessageHandler(filters.ALL & ~filters.COMMAND, handle_phone),
            ],
            STATE_REGION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_region),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
        ],
        allow_reentry=True,
    )

    app.add_handler(conv)

    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CommandHandler("export", export_csv))

    app.add_handler(MessageHandler(filters.Regex(f"^{re.escape(BTN_MY_INFO)}$"), my_info))
    app.add_handler(MessageHandler(filters.Regex(f"^{re.escape(BTN_HELP)}$"), help_msg))

<<<<<<< HEAD
    app.add_handler(MessageHandler(filters.Regex(f"^{re.escape(BTN_ADMIN_LIST)}$"), admin_list))
    app.add_handler(MessageHandler(filters.Regex(f"^{re.escape(BTN_ADMIN_EXPORT)}$"), admin_export_btn))

=======
>>>>>>> cd4359b74c56ceeb7cdfca6eaf141007fcf0ddf9
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, unknown_message))

    return app