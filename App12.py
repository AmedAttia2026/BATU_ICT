import os
import io
import asyncio
import requests
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# إعدادات البوت
TOKEN = "8067602225:AAHmpS7LtVLuy86RAT1ao6jmkykbHOWOZis"

# البيانات (كما هي في كودك الأصلي)
DATA = {
    "subjects": {
        "subject_iot": {
            "name": "💡 IoT Architecture & Protocols",
            "type": "submenu",
            "lectures": [
                {"n": "📝 IoT Lecture 1", "u": "https://it-department.cloud/files/materials/cTYrgEDfUF0WIbzOpLMprlU2juXDtvORzxAQDv6U.pdf"},
                {"n": "📄 IoT Sheet 1", "u": "https://it-department.cloud/files/materials/bJKhAbnUrbKQC52UljfTDgz0oCVGDXRShpCLNgFH.pdf"},
                {"n": "📑 Sheet 1 Answers", "u": "https://it-department.cloud/files/materials/GTBXsoMPpJ3XojwlYJMl3hCVgQN6kpZoqf5FKaUY.pdf"},
                # ... بقية المحاضرات تضاف هنا بنفس التنسيق
            ]
        },
        "subject_ai": {
            "name": "🧠 Artificial Intelligence",
            "type": "submenu",
            "lectures": [
                {"n": "📝 AI Lecture 1", "u": "https://it-department.cloud/files/materials/sMWIdOuHURclQwjAfXj26EUEG6wFHMyqIEIKQDP4.pdf"},
                {"n": "📄 AI Sheet 1", "u": "https://it-department.cloud/files/materials/JjVL9e70DyJMYe8ITyw8Uj2wxYd8HOa9EdSX5r7C.pdf"},
            ]
        },
        "subject_ccna_rs_iv": {
            "name": "📚 CCNA R&S IV",
            "url": "https://drive.google.com/uc?export=download&id=1B66Anzua3n-IdaR6ovCRWzrdpOMNSb7N",
            "filename": "CCNA_RS_IV_Course.pdf",
            "type": "direct_file"
        },
        # أضف بقية المواد هنا...
    }
}

# إعداد FastAPI والتطبيق
app = FastAPI()
ptb_app = Application.builder().token(TOKEN).build()

# --- وظائف المعالجة (Handlers) ---

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

    if data_key == "back_to_main":
        await start(update, context)
        return

    # منطق التحميل والإرسال (تم اختصاره هنا لسهولة القراءة، استخدم نفس منطقك الأصلي بالداخل)
    if data_key in subjects:
        subject = subjects[data_key]
        if subject.get('type') == 'submenu':
            # عرض القائمة الفرعية
            lectures = subject['lectures']
            keyboard = [[InlineKeyboardButton(l['n'], callback_data=f"dl_{data_key}_{i}")] for i, l in enumerate(lectures)]
            keyboard.append([InlineKeyboardButton("🔙 العودة", callback_data="back_to_main")])
            await query.edit_message_text(f"ملفات {subject['name']}:", reply_markup=InlineKeyboardMarkup(keyboard))
        elif subject.get('type') == 'direct_file':
            # تحميل مباشر
            res = requests.get(subject['url'])
            await context.bot.send_document(chat_id=update.effective_chat.id, document=io.BytesIO(res.content), filename=subject['filename'])

# تسجيل الـ Handlers
ptb_app.add_handler(CommandHandler("start", start))
ptb_app.add_handler(CallbackQueryHandler(handle_callback))

# --- مسارات Vercel ---

@app.post("/webhook")
async def process_update(request: Request):
    req_json = await request.json()
    update = Update.de_json(req_json, ptb_app.bot)
    await ptb_app.initialize()
    await ptb_app.process_update(update)
    return {"status": "ok"}

@app.get("/")
async def index():
    return {"message": "Bot is running on Webhook mode!"}
