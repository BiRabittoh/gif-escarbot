from telegram import Update
from telegram.ext import MessageHandler, ApplicationBuilder, CallbackQueryHandler, filters
from escarbot.config import TOKEN
from escarbot.inline import inline_handler
from escarbot.forward import forward, admin_forward
from escarbot.replace import replace

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CallbackQueryHandler(callback=inline_handler))
application.add_handler(MessageHandler(filters.ChatType.CHANNEL, forward))
application.add_handler(MessageHandler(filters.ChatType.PRIVATE, admin_forward))
application.add_handler(MessageHandler(filters.ChatType.GROUPS, replace))
application.run_polling(allowed_updates=[Update.CHANNEL_POST, Update.MESSAGE, Update.CALLBACK_QUERY])
