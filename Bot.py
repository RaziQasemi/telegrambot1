import datetime
import random
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
    ContextTypes,
)

from telegram.error import BadRequest
user_salavat_count = {}  # در بالای فایل بزار (global dict)
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_USERNAME = '@hasinyanon128'
TARGET_DATE = datetime.datetime(2025, 6, 14)

# --- لیست احادیث ---
hadith_list = [
    "❤️ هر که با علی دشمنی کند، با من دشمنی کرده است. (پیامبر اکرم)",
    "✨ علی با حق است و حق با علی است. (پیامبر اکرم)",
    "🌙 دوستی با علی عبادت است. (پیامبر اکرم)",
    "🌟 هر که علی را دوست دارد، در بهشت با من خواهد بود. (پیامبر اکرم)",
    "📚 علی باب علم من است. (پیامبر اکرم)",
    "🌸 علی جان! تو نور خدایی در زمین.",
    "🌼 ولایت علی، راه مستقیم خوشبختی است.",
    "🕊️ دل عاشق علی، همیشه آرامه.",
    "🌹 علی یعنی عشق تا ابد."
]

# --- متن درباره ---
ABOUT_TEXT = (
    "🤖 این ربات جهت یادآوری زمان باقی ماند تا عید غدیر و نشر احادیث ساخته شده.\n"
    "✨ به دست رضی الدین قاسمی، خادم حضرت فضه سلام الله علیها.\n"
    "📬 آیدی ارتباط: @QASEMI121\n"
    "جهت کمک به برپایی هرچه زیباتر عیدالله اکبر غدیر شماره کارت -6279611101066558-"
)

# --- لیست مداحی‌ها ---
madahi_list = [
    "https://t.me/hasinyanon128/4682",  # لینک مداحی اول
    "https://t.me/hasinyanon128/2672",  # لینک مداحی دوم
    "https://t.me/hasinyanon128/2110",  # لینک مداحی سوم
]

# --- کیبورد اصلی ---
def main_keyboard():
    return InlineKeyboardMarkup([ 
        [InlineKeyboardButton("🔄 بروزرسانی", callback_data="refresh")],
        [InlineKeyboardButton("📿 صلوات‌شمار", callback_data="salavat")],
        [InlineKeyboardButton("📚 کتاب", callback_data="books")],
        [InlineKeyboardButton("🎵 مداحی", callback_data="madahi")],
        [InlineKeyboardButton("📤 اشتراک‌گذاری", switch_inline_query="")],
        [InlineKeyboardButton("ℹ️ درباره", callback_data="about")]
        
    ])

# --- محاسبه شمارش معکوس ---
def get_countdown_text():
    now = datetime.datetime.now()
    delta = TARGET_DATE - now
    days_left = delta.days
    return f"⏳ {days_left} روز تا عید غدیر باقی مانده است!"

# --- حدیث رندوم ---
def get_random_hadith():
    return random.choice(hadith_list)

# --- ارسال مداحی رندوم ---
def get_random_madahi():
    return random.choice(madahi_list)

# --- بررسی عضویت در کانال ---
async def is_user_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_status = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=update.effective_user.id)
        return user_status.status in ['member', 'administrator', 'creator']
    except BadRequest:
        return False

# --- فرمان start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_user_member(update, context):
        await update.message.reply_text(f"🔒 لطفاً ابتدا در کانال عضو شوید:\n{CHANNEL_USERNAME}")
        return

    message = f"{get_countdown_text()}\n\n📜 حدیث روز:\n{get_random_hadith()}"
    await update.message.reply_text(message, reply_markup=main_keyboard())

# --- هندل دکمه‌ها ---
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not await is_user_member(update, context):
        await query.edit_message_text(f"🔒 لطفاً ابتدا در کانال عضو شوید:\n{CHANNEL_USERNAME}")
        return

    if query.data == "refresh":
        message = f"{get_countdown_text()}\n\n📜 حدیث روز:\n{get_random_hadith()}"
        await query.edit_message_text(message, reply_markup=main_keyboard())

    elif query.data == "about":
        await query.edit_message_text(ABOUT_TEXT, reply_markup=main_keyboard())

    elif query.data == "madahi":
        madahi = get_random_madahi()
        keyboard = [
            [InlineKeyboardButton("🎧 مداحی دیگه", callback_data="madahi")],
            [InlineKeyboardButton("🔙 برگشت", callback_data="refresh")]
        ]
        await query.edit_message_text(f"🎵 مداحی برات:\n{madahi}", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "books":
        keyboard = [[InlineKeyboardButton("📘 کتاب اول", url="https://t.me/hasinyanon128/4781")],
                    [InlineKeyboardButton("📗 کتاب دوم", url="https://t.me/hasinyanon128/4782")],
                    [InlineKeyboardButton("🔙 برگشت", callback_data="refresh")]]
        await query.edit_message_text("📚 کتاب‌های پیشنهادی:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "salavat":
        count = context.user_data.get("salavat_count", 0) + 1
        context.user_data["salavat_count"] = count

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📿 فرستادن صلوات", callback_data="salavat")],
            [InlineKeyboardButton("🔄 ریست صلوات‌ها", callback_data="reset_salavat")],
            [InlineKeyboardButton("🔙 برگشت", callback_data="refresh")]
        ])
        await query.edit_message_text(
            f"📿 تعداد صلوات‌های شما: {count}",
            reply_markup=keyboard
        )
        
    elif query.data == "reset_salavat":
        context.user_data["salavat_count"] = 0
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📿 فرستادن صلوات", callback_data="salavat")],
            [InlineKeyboardButton("🔄 ریست صلوات‌ها", callback_data="reset_salavat")],
            [InlineKeyboardButton("🔙 برگشت", callback_data="refresh")]
        ])
        await query.edit_message_text(
            "📿 صلوات‌ها ریست شدند. دوباره شروع کن!",
            reply_markup=keyboard
        )





# --- هندل اینلاین (اشتراک‌گذاری) با دکمه صلوات‌شمار ---
async def inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    message = f"{get_countdown_text()}\n\n📜 حدیث روز:\n{get_random_hadith()}"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📿 فرستادن صلوات", callback_data="salavat")]
    ])

    results = [
        InlineQueryResultArticle(
            id="1",
            title="ارسال شمارش معکوس عید غدیر",
            input_message_content=InputTextMessageContent(message),
            reply_markup=keyboard,
            description="⏳ ارسال متن روز همراه با حدیث و صلوات‌شمار",
        )
    ]
    await update.inline_query.answer(results, cache_time=1)


# --- اجرای ربات ---
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("countdown", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(InlineQueryHandler(inline))
app.run_polling()
