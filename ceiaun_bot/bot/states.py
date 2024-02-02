from telegram.ext import ConversationHandler

HOME, REQUEST_COURSE, GET_CHARTS, CONVERT_COURSE = map(chr, range(4))
END = ConversationHandler.END
