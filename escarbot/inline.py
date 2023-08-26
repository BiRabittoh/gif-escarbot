from telegram import Update
from telegram.ext import ContextTypes
from escarbot.config import INLINE_SEP
from escarbot.replace import feedback

inline_mapping = [ ("feedback", feedback) ]

async def inline_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data

    for t in inline_mapping:
        if data.startswith(t[0]):
            actual_data = data.split(INLINE_SEP, maxsplit=1)[1]
            await t[1](update, context, actual_data)
            return
        
    await query.answer("Questo tasto non fa nulla.")
    return
