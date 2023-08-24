from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from Config import INLINE_SEP
import logging, re, json
logger = logging.getLogger(__name__)

re_flags = re.I | re.M

replacers = [
    {
        "regex": re.compile(r"(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?", re_flags),
        "becomes": "https://y.outube.duckdns.org/{}",
    },
    {
        "regex": re.compile(r"(?:https?:\/\/)?(?:www\.)?twitter\.com\/(?:#!\/)?(.*)\/status(?:es)?\/([^\/\?\s]+)", re_flags),
        "becomes": "https://fxtwitter.com/{}/status/{}",
    },
]

link_message = "[.]({})"

def get_callback_data(feedback: bool) -> str:
    payload = { "feedback": feedback }
    return "feedback" + INLINE_SEP + json.dumps(payload)

def get_message_markup() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="✅", callback_data=get_callback_data(True)),
            InlineKeyboardButton(text="❌", callback_data=get_callback_data(False)),
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def format_template(template: str, regex_result) -> str:
    result_type = type(regex_result)
    if result_type is str:
        return template.format(regex_result)
    elif result_type is tuple or result_type is list:
        return template.format(*regex_result)
    elif result_type is dict:
        return template.format(**regex_result)
    else:
        return ""

def parse_text(message: str) -> list:
    output = []
    for site in replacers:
        regex = site["regex"]
        res = regex.findall(message)
        for r in res:
            link = format_template(site["becomes"], r)
            output.append(link)
    return output

async def replace(update: Update, _) -> None:
    try:
        links = parse_text(update.message.text)
    except TypeError:
        links = parse_text(update.message.caption)

    for link in links:
        logger.info(link)
        message = link_message.format(link)
        await update.message.reply_text(message, parse_mode="markdown", reply_markup=get_message_markup())

async def feedback(update: Update, _, data_json: str) -> None:
    data = json.loads(data_json)

    if data["feedback"]:
        await update.callback_query.answer("Bene!")
        await update.effective_message.edit_reply_markup()
        return

    await update.callback_query.answer("Ci ho provato...")
    await update.effective_message.delete()
    return
