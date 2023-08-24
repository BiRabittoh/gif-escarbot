from telegram.ext import MessageHandler, ApplicationBuilder, filters
from telegram import Update
from Config import TOKEN
from Replacer import replace
from Forwarder import forward, admin_forward

if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, forward))
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE, admin_forward))
    application.add_handler(MessageHandler(filters.CHAT & ~filters.COMMAND, replace))
    application.run_polling(allowed_updates=Update.MESSAGE)
