import os
import io
import asyncio
import requests
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==========================================
# 1. إعدادات البوت والبيانات
# ==========================================
TOKEN = "8067602225:AAHmpS7LtVLuy86RAT1ao6jmkykbHOWOZis"

DATA = {
    "subjects": {
        "subject_iot": {
            "name": "💡 IoT Architecture & Protocols",
            "type": "submenu",
            "lectures": [
                {"n": "📝 IoT Lecture 1", "u": "https://it-department.cloud/files/materials/cTYrgEDfUF0WIbzOpLMprlU2juXDtvORzxAQDv6U.pdf"},
                {"n": "📄 IoT Sheet 1", "u": "https://it-department.cloud/files/materials/bJKhAbnUrbKQC52UljfTDgz0oCVGDXRShpCLNgFH.pdf"},
                {"n": "📑 Sheet 1 Answers", "u": "https://it-department.cloud/files/materials/GTBXsoMPpJ3XojwlYJMl3hCVgQN6kpZoqf5FKaUY.pdf"},
                {"n": "📝 IoT Lecture 2", "u": "https://it-department.cloud/files/materials/LtAI0VIvOSstEKigPHc6wNlbNkD7U6s7XOa5AIZp.pdf"},
                {"n": "📄 IoT Sheet 2", "u": "https://it-department.cloud/files/materials/cPIMobis3lG2RYxeCloLqihgeO34SRyKqo70u9QD.pdf"},
                {"n": "📑 Sheet 2 Answers", "u": "https://it-department.cloud/files/materials/nc3m4w0OhUrBOlBwLsIH6JIL9zsBBySLGW0jVdyi.pdf"},
                {"n": "📝 IoT Lecture 3", "u": "https://it-department.cloud/files/materials/msy0QvHdCbbAOfKWnsvNzOvjjtR3E6qgaU5SCuRI.pdf"},
                {"n": "📄 IoT Sheet 3", "u": "https://it-department.cloud/files/materials/x3teKFNM8c7bPOrm3unl1kwv8WzqPGqRqWRSuo3l.pdf"},
                {"n": "📑 Sheet 3 Answers", "u": "https://it-department.cloud/files/materials/0y0xBtwp7t7RNgj7anfI5CemPJMXf3VkdJC0xuCE.pdf"},
                {"n": "📝 IoT Lecture 4", "u": "https://it-department.cloud/files/materials/tf7enMqRyvKzYA7WcWLRHBdQJ7mPkNBT5o6ZxF2C.pdf"},
                {"n": "📄 IoT Sheet 4", "u": "https://it-department.cloud/files/materials/8s41JawoYWZQH6ukcoIJHoaXcX14Lnf5oPduD9Zk.pdf"},
                {"n": "📑 Sheet 4 Answers", "u": "https://it-department.cloud/files/materials/CDsH5hyhTTQ14qAvPne5lVvp5VeCcaLtEYk1OKF3.pdf"},
                {"n": "📝 IoT Lecture 5", "u": "https://it-department.cloud/files/materials/MtFNu3V0cjcFQMedi2qkQKx6ruzpmkYY244XwFUQ.pdf"},
                {"n": "📄 IoT Sheet 5", "u": "https://it-department.cloud/files/materials/JlX2ivM60ONWRWA3I89C5rXyxRIzlDZnCueyHNzO.pdf"},
                {"n": "📑 Sheet 5 Answers", "u": "https://it-department.cloud/files/materials/CDsH5hyhTTQ14qAvPne5lVvp5VeCcaLtEYk1OKF3.pdf"},
                {"n": "📝 IoT Lecture 6", "u": "https://it-department.cloud/files/materials/Cjvox4AH59iZmNafZYmC6ib354K7AM0vMrEBUbPi.pdf"},
                {"n": "📄 IoT Sheet 6", "u": "https://it-department.cloud/files/materials/1Varqz1HDHC8qersjuLZK2NY8tZB4FNqI2FmGnbK.pdf"},
                {"n": "📑 Sheet 6 Answers", "u": "https://it-department.cloud/files/materials/8XpcENCpgG1uS9ZESmFO0ZtTMTAqyKxSS5ExXQj3.pdf"},
                {"n": "📝 IoT Lecture 7", "u": "https://it-department.cloud/files/materials/XgYTYyae7a56zTU3H4j5f7JAnE9l9nnp63gIurQU.pdf"},
                {"n": "📄 IoT Sheet 7", "u": "https://it-department.cloud/files/materials/1Varqz1HDHC8qersjuLZK2NY8tZB4FNqI2FmGnbK.pdf"},
                {"n": "📑 Sheet 7 Answers", "u": "https://it-department.cloud/files/materials/8XpcENCpgG1uS9ZESmFO0ZtTMTAqyKxSS5ExXQj3.pdf"},
                {"n": "📝 IoT Lecture 8", "u": "https://it-department.cloud/files/materials/9Z5xliYxaa8a3CjENEeNTGKt054PB90vTsKzXx7b.pdf"},
                {"n": "📄 IoT Sheet 8", "u": "https://it-department.cloud/files/materials/4mwaGpAQk93ACWumNL7jwbJ1KhbUAKVcg09HhyKN.pdf"},
                {"n": "📑 Sheet 8 Answers", "u": "https://it-department.cloud/files/materials/1JdGslNKYyiJixXP8wVCj1lLbKBfAfAiNgltqUWw.pdf"},
                {"n": "📝 IoT Lecture 9", "u": "https://it-department.cloud/files/materials/9bwaGNz89ZE3HnFZNkPWPtFauTOP6v4iQudR5Zdo.pdf"},
                {"n": "📄 IoT Sheet 9", "u": "https://it-department.cloud/files/materials/04nfzD9a0JbL0gOub6z6y0lq9DK0zUhOpy8ITIdJ.pdf"},
                {"n": "📑 Sheet 9 Answers", "u": "https://it-department.cloud/files/materials/VtZp1prBq3rKjEjhGh1sNcz9efeoE9pnxoNqlbxS.pdf"}
            ]
        },
        "subject_ai": {
            "name": "🧠 Artificial Intelligence",
            "type": "submenu",
            "lectures": [
                {"n": "📝 AI Lecture 1", "u": "https://it-department.cloud/files/materials/sMWIdOuHURclQwjAfXj26EUEG6wFHMyqIEIKQDP4.pdf"},
                {"n": "📄 AI Sheet 1", "u": "https://it-department.cloud/files/materials/JjVL9e70DyJMYe8ITyw8Uj2wxYd8HOa9EdSX5r7C.pdf"},
                {"n": "📝 AI Lecture 2", "u": "https://it-department.cloud/files/materials/kRBiIQQppQuUfFYg1GVicwoebsDHu3tOxQl6fhUD.pdf"},
                {"n": "📄 AI Sheet 2", "u": "https://it-department.cloud/files/materials/E2PfwLanrJ2G4gPQ3LHFw5zH4SvhijBEdniX3oum.pdf"},
                {"n": "📝 AI Lecture 3", "u": "https://it-department.cloud/files/materials/aOQi2APuqwXzSBnF8hdDNRJXf1nUBfIvSLpiWLBO.pdf"},
                {"n": "📄 AI Sheet 3", "u": "https://it-department.cloud/files/materials/0QqVKYNbpdIk3SH1sqPE3u514IljolPgWUFxys0Q.pdf"},
                {"n": "📝 AI Lecture 3_P2", "u": "https://it-department.cloud/files/materials/x6KkMIUwdpdyrmPC9JQy0xouEkge7wyQREbT9kZF.pdf"},
                {"n": "📄 AI Sheet 3_P2", "u": "https://it-department.cloud/files/materials/2cVQq4VTywo8SUSB0HunVzTrrspxwXuxTRNDQV99.pdf"},
                {"n": "📝 AI Lecture 4_P1", "u": "https://it-department.cloud/files/materials/6K92fbATBvM4cO0hOWVanxz6psDqS9HXZjpLBWhN.pdf"},
                {"n": "📄 AI Sheet 4_P1", "u": "https://it-department.cloud/files/materials/BjeCstBdgCXaiLqUZNfXVjpGEGdOra0xl6mpBSHp.pdf"},
                {"n": "📝 AI Lecture 4_P2", "u": "https://it-department.cloud/files/materials/vySnm37LXEVQzq11jh0gmaLAZ6mnoOQJ4dROiSwm.pdf"},
                {"n": "📄 AI Sheet 4_P2", "u": "https://it-department.cloud/files/materials/uHvBnVB3moRoWhokP2BHhMemhcoFO6Ct6gLaG8nN.pdf"},
                {"n": "📝 AI Lecture 5", "u": "https://it-department.cloud/files/materials/DJOUhazcS17FJF2Q5Z6EiGI5dJq7sdu2nSI9BZk6.pdf"},
                {"n": "📄 AI Sheet 5", "u": "https://it-department.cloud/files/materials/tnx2fbeIDuMJfJK0lpoOiwzEEZMAqUnJXKBTSuJW.pdf"},
                {"n": "📝 AI Lecture 6", "u": "https://it-department.cloud/files/materials/qtUhWcYObMdw6bkXdTihp2qkT34Q7sqySbKkE3Xp.pdf"},
                {"n": "📄 AI Sheet 6", "u": "https://it-department.cloud/files/materials/fDjcjvfBNQxR8jUhGDgWibMRcM2vh0NpoTwGoN6y.pdf"},
                {"n": "📝 AI Lecture 7", "u": "https://www.batechu.com/files/materials/MWSnzftVXDIW6EQYjeP7myElaLwFFFC2Sed4vHpR.pdf"},
                {"n": "📄 AI Sheet 7", "u": "https://www.batechu.com/files/materials/M3T6PapLhiZYgpREy5DcFqL9o3dbNsrsdDpyazAC.pdf"}
            ]
        },
        "subject_ccna_rs_iv": {
            "name": "📚 CCNA R&S IV",
            "url": "https://drive.google.com/uc?export=download&id=1B66Anzua3n-IdaR6ovCRWzrdpOMNSb7N",
            "filename": "CCNA_RS_IV_Course.pdf",
            "type": "direct_file"
        },
        "subject_ccna_cyber": {
            "name": "🔒 CCNA Cybersecurity",
            "url": "https://drive.google.com/uc?export=download&id=18jqXXhKe-iGEvCDkfc_QZ3QqgMXgL3an",
            "filename": "CCNA_Cybersecurity.pdf",
            "type": "direct_file"
        },
        "subject_server_admin": {
            "name": "🖥️ Server Administration",
            "url": "https://drive.google.com/uc?export=download&id=1gzD08vhVKqRYsJPj9b3az560TqxqHAvB",
            "filename": "Server_Admin.pdf",
            "type": "direct_file"
        },
        "subject_encryption": {
            "name": "🔐 Encryption Algorithm",
            "url": "https://drive.google.com/uc?export=download&id=1a_TIGB3FfRXp0ZclR3rr-Jn9EwtoJ8Oy",
            "filename": "Encryption.pdf",
            "type": "direct_file"
        }
    }
}

# ==========================================
# 2. الدوال المساعدة لتحميل وإرسال الملفات
# ==========================================

async def download_and_send(chat_id, context, url, filename, caption):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        file_io = io.BytesIO(response.content)
        file_io.name = filename
        await context.bot.send_document(chat_id=chat_id, document=file_io, caption=caption)
        return True
    except Exception as e:
        print(f"Error sending file: {e}")
        return False

# ==========================================
# 3. معالجات البوت (Handlers)
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_text = f"👋 مرحباً بك يا <b>{user.mention_html()}</b>! ✨\n\nأنا مساعدك الدراسي الذكي. اختر المادة 👇:"
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
    chat_id = update.effective_chat.id

    if data_key == "back_to_main":
        await start(update, context)
        return

    # تنزيل الكل
    if data_key.startswith("all_"):
        subject_key = data_key.replace("all_", "")
        subject = DATA['subjects'].get(subject_key)
        msg = await query.message.reply_html(f"🚀 جاري إرسال ملفات <b>{subject['name']}</b>...")
        
        if subject['type'] == 'direct_file':
            await download_and_send(chat_id, context, subject['url'], subject['filename'], f"✅ {subject['name']}")
        else:
            for lec in subject['lectures']:
                await download_and_send(chat_id, context, lec['u'], f"{lec['n']}.pdf", f"✅ {lec['n']}")
                await asyncio.sleep(0.5) 
        await msg.edit_text("✨ تم الإرسال بنجاح!")
        return

    # عرض الملفات المتاحة
    if data_key in DATA['subjects'] and DATA['subjects'][data_key]['type'] == 'submenu':
        subject = DATA['subjects'][data_key]
        keyboard = []
        for i in range(0, len(subject['lectures']), 2):
            row = [InlineKeyboardButton(subject['lectures'][i]['n'], callback_data=f"dl_{data_key}_{i}")]
            if i + 1 < len(subject['lectures']):
                row.append(InlineKeyboardButton(subject['lectures'][i+1]['n'], callback_data=f"dl_{data_key}_{i+1}"))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("📥 تنزيل كل الملفات", callback_data=f"all_{data_key}")])
        keyboard.append([InlineKeyboardButton("🔙 العودة", callback_data="back_to_main")])
        await query.edit_message_text(text=f"📂 ملفات {subject['name']}:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data_key.startswith("dl_"):
        parts = data_key.split("_")
        subject_key, lec_idx = "_".join(parts[1:-1]), int(parts[-1])
        lec = DATA['subjects'][subject_key]['lectures'][lec_idx]
        await download_and_send(chat_id, context, lec['u'], f"{lec['n']}.pdf", f"✅ {lec['n']}")

    elif data_key in DATA['subjects']:
        subject = DATA['subjects'][data_key]
        await download_and_send(chat_id, context, subject['url'], subject['filename'], f"✅ {subject['name']}")

# ==========================================
# 4. إعداد FastAPI والـ Lifespan (دمج كامل)
# ==========================================

bot_app = Application.builder().token(TOKEN).build()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # تشغيل البوت مرة واحدة عند بدء السيرفر
    await bot_app.initialize()
    await bot_app.start()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CallbackQueryHandler(handle_callback))
    yield
    # إغلاق نظيف للبوت
    await bot_app.stop()
    await bot_app.shutdown()

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def webhook_handler(request: Request):
    data = await request.json()
    try:
        # استخدام الـ Constructor المباشر لـ v20+ كما اقترحت
        update = Update(**data)
        await bot_app.process_update(update)
    except Exception as e:
        print(f"Webhook Error: {e}")
    
    return Response(status_code=200)

@app.get("/")
def index():
    return {"message": "Server is running. Send updates to /webhook"}
