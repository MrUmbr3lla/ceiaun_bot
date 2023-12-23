from texts import *

Tk = config('token')
users_result = []


#finding empty rows in excel file
def find_empty_row(sheet: Worksheet) -> int:
    row_number = 3
    while True:
        if sheet[f"A{row_number}"].value is None:
            return row_number

        row_number += 1


workbook = load_workbook('base.xlsx')
worksheet = workbook.active


#bot commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=start_command_message)



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text =help_command_message)



#bot responses
def handle_responses(text: str) -> str:

    proccessed: str = text


    #convert course name for Amoozeshyar
    if 'تبدیل' in proccessed:
        chars = list(proccessed)
        course_name = chars[5:]
        if course_name[-1] != ' ':
            course_name.append(' ')
        modified_name = ''.join([sub
                                 .replace(' ', '%')
                                 .replace('ی' , '%')
                                 .replace('ک' , '%')
                                 .replace('ي' , '%')
                                 .replace('ك' , '%')
                                 for sub in course_name])
        return modified_name

    user_text = proccessed.split('+')


    if len(user_text) != 4:
        return incorrect_length_message


    
    student_name = user_text[0].strip()
    student_id = str(unidecode(user_text[1].strip()))
    student_course = user_text[2].strip()
    student_course_id = str(unidecode(user_text[3].strip()))


    if student_name.isnumeric():
        return incorrect_username_message
    
    if (not student_id.isnumeric()) or (len(student_id) not in [8, 11, 14]):
        return incorrect_studentid_message
    
    if student_course.isnumeric():
        return incorrect_course_message
    
    if not student_course_id.isnumeric():
        return incorrect_courseid_message


    #adding data to excel file
    row_number = find_empty_row(worksheet)
    worksheet[f"A{row_number}"] = student_name
    worksheet[f"B{row_number}"] = student_id
    worksheet[f"C{row_number}"] = student_course
    worksheet[f"D{row_number}"] = student_course_id
    workbook.save('base.xlsx')
    return recieved_request_message


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
