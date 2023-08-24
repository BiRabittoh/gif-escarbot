from telegram.ext import ContextTypes, MessageHandler, ApplicationBuilder, CallbackQueryHandler, filters
from telegram import Update
from Config import TOKEN, INLINE_SEP
from Replacer import replace, feedback
from Forwarder import forward, admin_forward

inline_mapping = [ ("feedback", feedback) ]

async def inline_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data

    for t in inline_mapping:
        if data.startswith(t[0]):
            actual_data = data.split(INLINE_SEP, maxsplit=1)[1]
            await t[1](update, context, actual_data)
            return
        
    await query.answer("Questo tasto non fa nulla.")
    return

if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CallbackQueryHandler(callback=inline_keyboard))
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, forward))
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE, admin_forward))
    application.add_handler(MessageHandler(filters.ChatType.GROUPS, replace))
    application.run_polling(allowed_updates=[Update.CHANNEL_POST, Update.MESSAGE, Update.CALLBACK_QUERY])
