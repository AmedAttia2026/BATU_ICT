import os
import io
import requests
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# ==========================================
# 1. إعدادات البوت والبيانات ⚙️
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
# 2. منطق عمل البوت 🤖
# ==========================================

async def start(update: Update, context: object) -> None:
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

async def handle_callback(update: Update, context: object) -> None:
    query = update.callback_query
    await query.answer()
    
    data_key = query.data
    subjects = DATA['subjects']

    # --- خيار تنزيل كل ملفات مادة محددة 📥 ---
    if data_key.startswith("all_"):
        subject_key = data_key.replace("all_", "")
        subject = subjects.get(subject_key)
        
        if not subject: return

        status_msg = await query.message.reply_html(f"🚀 جاري إرسال كافة ملفات <b>{subject['name']}</b>...")
        
        try:
            if subject.get('type') == 'direct_file':
                res = requests.get(subject['url'], stream=True)
                await context.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=InputFile(io.BytesIO(res.content), filename=subject['filename']),
                    caption=f"✅ مادة: {subject['name']}"
                )
            elif subject.get('type') == 'submenu':
                for lecture in subject['lectures']:
                    await context.bot.send_document(
                        chat_id=update.effective_chat.id,
                        document=lecture['u'],
                        caption=f"✅ {lecture['n']}"
                    )
                    await asyncio.sleep(0.4) # تأخير بسيط لتجنب سبام تليجرام
            
            await status_msg.edit_text(f"✨ تم إرسال جميع ملفات <b>{subject['name']}</b> بنجاح! ✅", parse_mode='HTML')
        except Exception as e:
            await query.message.reply_text(f"❌ خطأ: {e}")
        return

    # زر العودة 🔙
    if data_key == "back_to_main":
        await start(update, context)
        return

    # عرض القائمة الفرعية للمادة (مثل AI و IoT)
    if data_key in subjects and subjects[data_key].get('type') == 'submenu':
        subject = subjects[data_key]
        keyboard = []
        lectures = subject['lectures']
        
        # ترتيب الأزرار (2 في كل صف)
        for i in range(0, len(lectures), 2):
            row = [InlineKeyboardButton(lectures[i]['n'], callback_data=f"dl_{data_key}_{i}")]
            if i + 1 < len(lectures):
                row.append(InlineKeyboardButton(lectures[i+1]['n'], callback_data=f"dl_{data_key}_{i+1}"))
            keyboard.append(row)
        
        # زر "تنزيل الكل" للمادة
        keyboard.append([InlineKeyboardButton(f"📥 تنزيل كل ملفات {subject['name']}", callback_data=f"all_{data_key}")])
        keyboard.append([InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_to_main")])
        
        await query.edit_message_text(
            text=f"{subject['name']} ⚙️\n\nإليك الملفات المتاحة. اختر ملفاً أو قم بتنزيل الكل 👇:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )

    # تحميل ملف فردي من القائمة الفرعية
    elif data_key.startswith("dl_"):
        parts = data_key.split("_")
        subject_key = "_".join(parts[1:-1]) 
        lecture_idx = int(parts[-1])
        lecture = subjects[subject_key]['lectures'][lecture_idx]
        msg = await query.message.reply_html(f"⏳ جاري إرسال: <b>{lecture['n']}</b>...")
        try:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=lecture['u'], caption=f"✅ {lecture['n']}")
            await msg.delete()
        except: await query.message.reply_text("❌ فشل الإرسال.")

    # عرض مادة ذات ملف واحد (Google Drive)
    elif data_key in subjects:
        subject = subjects[data_key]
        btns = [
            [InlineKeyboardButton(f"⬇️ تنزيل {subject['name']}", callback_data=f"file_{data_key}")],
            [InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_to_main")]
        ]
        await query.edit_message_text(
            f"📚 مادة: <b>{subject['name']}</b>\nالملف المتاح: <b>{subject['filename']}</b>",
            reply_markup=InlineKeyboardMarkup(btns),
            parse_mode='HTML'
        )

    # تنفيذ تحميل ملف من Drive
    elif data_key.startswith("file_"):
        s_key = data_key.replace("file_", "")
        subject = subjects[s_key]
        msg = await query.edit_message_text(f"⏳ جاري تحميل <b>{subject['name']}</b>...")
        try:
            res = requests.get(subject['url'], stream=True)
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=InputFile(io.BytesIO(res.content), filename=subject['filename']),
                caption=f"✅ تم تحميل {subject['name']}"
            )
            await msg.delete()
        except: await query.message.reply_text("❌ حدث خطأ.")

# ==========================================
# 3. التشغيل 🚀
# ==========================================

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    print("🚀 البوت يعمل الآن بنظام Polling...")
    application.run_polling()

if __name__ == "__main__":
    main()
