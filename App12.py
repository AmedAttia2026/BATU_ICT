import os
import io
import requests
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

TOKEN = os.environ.get("BOT_TOKEN")  # ضع توكن البوت هنا

DATA = {
    "subjects": {
        "subject_iot": {
            "name": "💡 IoT Architecture & Protocols",
            "type": "submenu",
            "lectures": [
                {"n": "📝 IoT Lecture 1", "u": "https://it-department.cloud/files/materials/cTYrgEDfUF0WIbzOpLMprlU2juXDtvORzxAQDv6U.pdf"}
            ]
        }
    }
}

async def start(update: Update, context):
    keyboard = [[InlineKeyboardButton(v['name'], callback_data=k)] for k,v in DATA['subjects'].items()]
    await update.message.reply_html("👋 اختر المادة:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_callback(update: Update, context):
    query = update.callback_query
    await query.answer()
    if query.data in DATA['subjects']:
        subject = DATA['subjects'][query.data]
        for lecture in subject['lectures']:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=lecture['u'], caption=lecture['n'])

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("🚀 البوت شغال الآن باستخدام Polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
