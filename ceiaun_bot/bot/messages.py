# Home
START_COMMAND = """🔻قابل توجه دانشجویان :

لطفا قبل از استفاده از ابزار های ربات، فایل راهنمای استفاده از آن (تصویر بالا) را مطالعه نمایید.
"""

HOME_SHORT = "به صفحه اصلی بازگشتید 👇"

# Request course
REQUEST_COMMAND = """اگر در زمان انتخاب واحد موفق به اخذ درسی نشدید، لطفا درخواست خود را به فرمت گفته شده مانند تصویر بالا ارسال کنید. (در صورتی که ترم آخر هستید به صورت خصوصی به آیدی @mob_gh پیام دهید)

<b>نام و نام خانوادگی + شماره دانشجویی + نام درس + کد ارائه
</b>

<tg-spoiler>نمونه: نیما کیانی + 39915042054099 + ساختمان داده + 2323185</tg-spoiler>

نکات مهم:
▪️صرفا برای دروسی درخواست ارسال کنید که در زمان ثبت نام، <u>تمامی گروه‌های دیگر آن نیز تکمیل شده باشند</u> و ارائه دهنده آن، گروه کارشناسی مهندسی کامپیوتر باشد. (<b>دروس عمومی و پایه مانند ریاضی و فیزیک ارتباطی به گروه کارشناسی مهندسی کامپیوتر ندارد</b>)

▪️دقت داشته باشید که در زمان ارسال درخواست، اطلاعات با استفاده از علامت «+» از یکدیگر جدا شده باشند.

▪️پس از ارسال درخواست، بررسی ظرفیت درس مورد نظر و اخذ آن بر عهده دانشجو است. لطفا در مورد زمان افزایش ظرفیت سوال نفرمایید."""

REQUEST_INCORRECT_LENGTH = """❌ لطفا درخواست خود را طبق فرمت گفته شده مجدد ارسال کنید.


<b>نام و نام خانوادگی + شماره دانشجویی + نام درس + کد ارائه
</b>

<tg-spoiler>نمونه: نیما کیانی + 39915042054099 + ساختمان داده + 2323185</tg-spoiler>"""

# Student name
REQUEST_INCORRECT_USERNAME = "❗️ لطفا نام و نام خانوادگی خود را به درستی وارد کنید و درخواست خود را مجدد ارسال نمایید "

# Student id
REQUEST_INCORRECT_STUDENT_ID = "❗️ لطفا شماره دانشجویی خود را به درستی وارد کنید و درخواست خود را مجدد ارسال نمایید "
REQUEST_INCORRECT_STUDENT_ID_CODE_MELLI = "❗️ لطفا شماره دانشجویی خود را وارد کنید و درخواست خود را مجدد ارسال نمایید. کد ملی مورد قبول نمی‌باشد."

# Course name
REQUEST_INCORRECT_COURSE = "❗️ لطفا نام درس را به درستی وارد کنید و درخواست خود را مجدد ارسال نمایید "
REQUEST_INCORRECT_COURSE_OTHER_DEPARTMENT = """❗️لطفا تنها دروس تخصصی کامپیوتر را ارسال کنید و درخواست خود را مجدد ارسال نمایید.

▪️برای دروس فیزیک به دکتر دائی محمد مراجعه نمایید.
▫️برای دروس ریاضی به دکتر جعفری (مدیر گروه ریاضی) مراجعه نمایید.
▪️برای دروس معارف به دکتر شریعتی و برای درس انس با قرآن به خانم حاج امینی مراجعه نمایید.
▫️برای دروس ادبیات، زبان، تاریخ تمدن به خانم لسانی مراجعه نمایید.
▪️برای دروس تربیت بدنی و ورزش به دکتر افتخاری مراجعه نمایید.

<a href='https://t.me/ceiaun/1011'>دفترچه تلفن دانشگاه</a>"""

# Course id
REQUEST_INCORRECT_COURSE_ID = "❗️ لطفا کد ارائه درس را به درستی وارد کنید و درخواست خود را مجدد ارسال نمایید "
REQUEST_INCORRECT_COURSE_ID_INSTEAD = """❗️لطفا کد ارائه درس را به درستی وارد کنید و درخواست خود را مجدد ارسال نمایید.

💡کد درس با کد ارائه درس متفاوت است، لطفا کد ارائه درس را ارسال نمایید."""

REQUEST_RECEIVED_REQUEST = """درخواست شما دریافت شد ✅

📌پس از ارسال درخواست خود، بررسی ظرفیت درس مورد نظر و اخذ آن بر عهده دانشجو است. لطفا در مورد زمان افزایش ظرفیت سوال نفرمایید.

🔻درخواست بعدی خود را ارسال نمایید یا با استفاده از دکمه "برگشت" به صفحه اصلی برگردید:"""

# Convert name
CONVERT_NAME_COMMAND = """🔻جهت تبدیل نام دروس کافیست نام درس مورد نظر خود را وارد کنید. (نمونه در تصویر بالا)"""
CONVERT_NAME_RESULT = """نام درس با موفقیت تبدیل شد ✅

نام درس تغییر یافته :
{result}

: در صورتی که قصد تغییر نام درس دیگری رو دارید، نام درس مورد نظر خود را وارد کنید یا از گزینه «برگشت» استفاده کنید"""
# Chart
CHART_SELECT_ORIENT = """💠 نحوه تعیین #گرایش رشته مهندسی کامپیوتر

🔹گرایش دانشجویان ورودی 95 به بعد در زمان ثبت نام مشخص نمی‌باشد، لذا تعیین گرایش دانشجو با توجه به اولین درس تخصصی انجام خواهد شد. در صورت عدم رعایت این مورد، دانشجو در زمان فارغ التحصیلی با مشکل مواجه خواهد شد.

🔹دو #گرایش نرم افزار و فناوری اطلاعات در 7 درس سه واحدی تفاوت دارند که این دروس را از فایل لیست دروس گرایش مورد نظر قابل مشاهده می‌باشد. (جدول دروس تخصصی)

📌 تاکید می‌گردد که اخذ درس سه واحدی از گرایش مخالف به عنوان واحد #اختیاری، تنها پس از مشخص شدن گرایش دانشجو و اخذ اولین درس تخصصی از آن گرایش امکان پذیر خواهد بود.

<a href="https://t.me/ceiaun">کانال دانشجویان مقطع کارشناسی کامپیوتر</a>
@ceiaun"""

CHART_SE_CAPTION = """📌 لیست دروس و چارت پیشنهادی رشته مهندسی کامیپوتر - گرایش نرم افزار

پیش نیاز دروس از هر دو فایل بررسی شود.

<a href="https://t.me/ceiaun">کانال دانشجویان مقطع کارشناسی کامپیوتر</a>
@ceiaun"""

CHART_IT_CAPTION = """📌 لیست دروس و #چارت پیشنهادی رشته مهندسی کامیپوتر - #گرایش فناوری اطلاعات (IT)

پیش نیاز دروس از هر دو فایل بررسی شود.

<a href="https://t.me/ceiaun">کانال دانشجویان مقطع کارشناسی کامپیوتر</a>
@ceiaun"""

# Admin
ADMIN_HOME = "پنل ادمین:"
ADMIN_STAT = "تعداد کاربران: {users_count}"
ADMIN_GET_FILE_TITLE = "عنوان فایل را ارسال کنید:"
