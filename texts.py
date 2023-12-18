#imports
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from decouple import config
from unidecode import unidecode
from openpyxl.reader.excel import load_workbook
from openpyxl.worksheet.worksheet import Worksheet



start_command_message = """

🔻فرمت درخواست به شکل زیر می‌باشد. در صورتی که ترم آخر هستید، به صورت جداگانه به ادمین اطلاع دهید.

نام و نام خانوادگی + شماره دانشجویی + نام درس + کد ارائه

نیاز به راهنمایی /help

@mob_gh

 """


help_command_message = """

temporary disabled

"""


incorrect_length_message = " ❌ لطفا درخواست خود را طبق فرمت گفته شده ارسال کنید "

incorrect_username_message = "❗️ لطفا نام و نام خانوادگی خود را به درستی وارد کنید "

incorrect_studentid_message = "❗️ لطفا شماره دانشجویی خود را به درستی وارد کنید "

incorrect_course_message = "❗️ لطفا نام درس را به درستی وارد کنید "

incorrect_courseid_message = "❗️ لطفا کد ارائه درس را به درستی وارد کنید "

recieved_request_message = " درخواست شما دریافت شد ✅ "