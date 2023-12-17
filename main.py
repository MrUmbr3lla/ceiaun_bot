from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from decouple import config
from unidecode import unidecode
from openpyxl.reader.excel import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

Tk = config('token')
BOT_USERNAME: Final = '@iaun_computer_faculty_bot'
users_result = []


def find_empty_row(sheet: Worksheet) -> int:
    row_number = 3
    while True:
        if sheet[f"A{row_number}"].value is None:
            return row_number

        row_number += 1


workbook = load_workbook('base.xlsx')
worksheet = workbook.active


#bot part
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""🔻فرمت درخواست به شکل زیر می‌باشد. در صورتی که ترم آخر می‌باشید، به صورت جداگانه ذکر کنید.

نام و نام خانوادگی + شماره دانشجویی + نام درس + کد ارائه""",)



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text = 
"""برای اطلاعات بیشتر به آیدی زیر پیام دهید :
@nima_kiani""")



#responses
def handle_responses(text: str) -> str:

    proccessed: str = text
    user_text = proccessed.split('+')


    if len(user_text) != 4:
        return """
❌ لطفا درخواست خود را طبق فرمت گفته شده ارسال کنید
راهنمایی /help
"""


    
    student_name = user_text[0].strip()
    student_id = str(unidecode(user_text[1].strip()))
    student_course = user_text[2].strip()
    student_course_id = str(unidecode(user_text[3].strip()))


    if student_name.isnumeric():
        return "❗️ لطفا نام و نام خانوادگی خود را به درستی وارد کنید"
    
    if not student_id.isnumeric():
        return "❗️ لطفا شماره دانشجویی خود را به درستی وارد کنید"
    
    if student_course.isnumeric():
        return "❗️ لطفا نام درس را به درستی وارد کنید"
    
    if not student_course_id.isnumeric():
        return "❗️ لطفا کد ارائه درس را به درستی وارد کنید"

    if len(student_id) != 14:
        return "❗️ لطفا شماره دانشجویی خود را به درستی وارد کنید"
    
    row_number = find_empty_row(worksheet)
    worksheet[f"A{row_number}"] = student_name
    worksheet[f"B{row_number}"] = student_id
    worksheet[f"C{row_number}"] = student_course
    worksheet[f"D{row_number}"] = student_course_id
    workbook.save('base.xlsx')
    return "✅ درخواست شما دریافت شد"


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    users_id: str = update.message.from_user.username
    print(f'user`s id is = {users_id}')
    
    print(f' user{update.message.chat.id} in {message_type}: {text}')

    response: str = handle_responses(text)

    await update.message.reply_text(response)



async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print(f'update {update} caused error {context.error}')


if __name__ == '__main__':
    print('starting bot ...')
    app = Application.builder().token(Tk).build()





#commands
    app.add_handlers([
        CommandHandler('start', start_command),
        CommandHandler('help', help_command)
    ])

#messages
    app.add_handler(MessageHandler(filters.TEXT , handle_messages))

#errors
app.add_error_handler(error)

#polls the bot
print('polling ...')
app.run_polling(poll_interval=3)
