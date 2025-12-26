import os
import io
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==========================================
# 1. إعدادات البوت والبيانات ⚙️
# ==========================================

TOKEN = os.environ.get("BOT_TOKEN")  # ضع توكن البوت في Environment Variable باسم BOT_TOKEN

DATA = {
    "subjects": {
        "subject_iot": {
            "name": "💡 IoT Architecture & Protocols",
            "type": "submenu",
            "lectures": [
                {"n": "📝 IoT Lecture 1", "u": "https://it-department.cloud/files/materials/cTYrgEDfUF0WIbzOpLMprlU2juXDtvORzxAQDv6U.pdf"},
                {"n": "📄 IoT Sheet 1", "u": "https://it-department.cloud/files/materials/bJKhAbnUrbKQC52UljfTDgz0oCVGDXRShpCLNgFH.pdf"}
                # أضف باقي الملفات هنا
            ]
        },
        "subject_ai": {
            "name": "🧠 Artificial Intelligence",
            "type": "submenu",
            "lectures": [
                {"n": "📝 AI Lecture 1", "u": "https://it-department.cloud/files/materials/sMWIdOuHURclQwjAfXj26EUEG6wFHMyqIEIKQDP4.pdf"}
                # أضف باقي الملفات هنا
            ]
        }
    }
}

# ==========================================
# 2. منطق عمل البوت 🤖
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_text = (
        f"👋 مرحباً بك يا <b>{user.mention_html()}</b>! ✨\n\n"
        "أنا مساعدك الدراسي الذكي. 📚\n"
        "اختر المادة التي ترغب في الحصول على ملفاتها 👇:"
    )
    keyboard = [[InlineKeyboardButton(v['name'], callback_data=k)] for k, v in DATA['subjects'].items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.message.reply_html(welcome_text, reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data_key = query.data
    subjects = DATA['subjects']

    # عرض القائمة الفرعية للمادة
    if data_key in subjects and subjects[data_key].get('type') == 'submenu':
        subject = subjects[data_key]
        keyboard = []
        lectures = subject['lectures']
        for i in range(0, len(lectures), 2):
            row = [InlineKeyboardButton(lectures[i]['n'], callback_data=f"dl_{data_key}_{i}")]
            if i + 1 < len(lectures):
                row.append(InlineKeyboardButton(lectures[i+1]['n'], callback_data=f"dl_{data_key}_{i+1}"))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton(f"📥 تنزيل كل ملفات {subject['name']}", callback_data=f"all_{data_key}")])
        keyboard.append([InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_to_main")])
        await query.edit_message_text(
            text=f"{subject['name']} ⚙️\n\nإليك الملفات المتاحة. اختر ملفاً أو قم بتنزيل الكل 👇:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )

    # تحميل ملف فردي
    elif data_key.startswith("dl_"):
        parts = data_key.split("_")
        subject_key = "_".join(parts[1:-1])
        lecture_idx = int(parts[-1])
        lecture = subjects[subject_key]['lectures'][lecture_idx]
        msg = await query.message.reply_html(f"⏳ جاري إرسال: <b>{lecture['n']}</b>...")
        try:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=lecture['u'], caption=f"✅ {lecture['n']}")
            await msg.delete()
        except:
            await query.message.reply_text("❌ فشل الإرسال.")

    # تنزيل كل الملفات
    elif data_key.startswith("all_"):
        subject_key = data_key.replace("all_", "")
        subject = subjects[subject_key]
        for lecture in subject['lectures']:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=lecture['u'], caption=f"✅ {lecture['n']}")
        await query.message.reply_text(f"✨ تم إرسال جميع ملفات {subject['name']} بنجاح! ✅")

    # زر العودة
    elif data_key == "back_to_main":
        await start(update, context)

# ==========================================
# 3. التشغيل باستخدام Webhook 🚀
# ==========================================

def main():
    PORT = int(os.environ.get("PORT", 8443))
    DOMAIN = os.environ.get("PROJECT_DOMAIN")  # موجود تلقائياً على Railway

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))

    print(f"🚀 البوت يعمل الآن باستخدام Webhook على https://{DOMAIN}.up.railway.app/{TOKEN}")
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://{DOMAIN}.up.railway.app/{TOKEN}"
    )

if __name__ == "__main__":
    main()
