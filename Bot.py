import os
import openai
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# ---------- Prompt Generators ----------
def generate_prompt(mode, user_input):
    if mode == "emotional":
        return f"""تو یک مشاور احساسی مهربان هستی. به زبان ساده و همدلانه پاسخ بده.
سپس اگر حدیث مرتبطی از حضرت علی علیه‌السلام درباره آرامش، صبر یا امیدواری وجود دارد، همراه با منبع معتبر آن ذکر کن.
پیام کاربر: {user_input}"""

    elif mode == "religious":
        return f"""تو یک مشاور دینی شیعه هستی. به زبان ساده و مستند جواب بده.
فقط از منابع شیعه استفاده کن. در انتهای پاسخ، اگر حدیثی از حضرت علی علیه‌السلام مرتبط با موضوع هست، با ذکر منبع معتبر بیار.
سوال: {user_input}"""

    elif mode == "growth":
        return f"""تو یک مشاور رشد فردی هستی. به زبان انگیزشی، علمی و انسانی جواب بده.
در پایان، اگر حدیثی از حضرت علی علیه‌السلام درباره رشد، یادگیری، حکمت یا تلاش وجود دارد، بیار و منبع معتبرش رو بنویس.
موضوع: {user_input}"""

# ---------- GPT Call ----------

async def ask_gpt(prompt):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

    return response['choices'][0]['message']['content']

# ---------- Telegram Handlers ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("💬 مشاوره احساسی")],
        [KeyboardButton("🕌 مشاوره دینی")],
        [KeyboardButton("🧠 رشد فردی")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("سلام عزیز دلم 😊\nچه نوع مشاوره‌ای می‌خوای؟", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "💬 مشاوره احساسی":
        context.user_data["mode"] = "emotional"
        await update.message.reply_text("خب عزیز دلم، حرف دلتو بزن 💌")

    elif text == "🕌 مشاوره دینی":
        context.user_data["mode"] = "religious"
        await update.message.reply_text("سوال دینی‌ت رو بپرس، فقط از منابع شیعه جواب می‌دم 🕌")

    elif text == "🧠 رشد فردی":
        context.user_data["mode"] = "growth"
        await update.message.reply_text("بگو ببینم دنبال چه جور پیشرفتی هستی؟ 💡")

    else:
        mode = context.user_data.get("mode")
        if not mode:
            await update.message.reply_text("لطفاً اول نوع مشاوره رو انتخاب کن از منو بالا ⬆️")
            return

        prompt = generate_prompt(mode, text)
        reply = await ask_gpt(prompt)
        await update.message.reply_text(reply)

# ---------- Bot Run ----------
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 ربات روشنه...")
    app.run_polling()

if __name__ == "__main__":
    main()
