from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from escarbot.config import INLINE_SEP, FEEDBACK_TIMEOUT
import logging, re, json
from asyncio import sleep
logger = logging.getLogger(__name__)

re_flags = re.I | re.M

def get_human_readable(input_str: str, indicator: str, offset: int = 0) -> (int, int):
    try:
        result = int(input_str[offset:].split(indicator, maxsplit=1)[0])
        return result, len(str(result)) + len(indicator)
    except ValueError:
        return 0, 0

youtube_timestamp_regex = re.compile(r"(?:&|\?)t=(\d*h?\d*m?\d*s?)", re_flags)
def youtube_timestamp(input_str: str) -> str:
    result = youtube_timestamp_regex.findall(input_str)
    try:
        input_string = result[0]
        seconds = int(input_string)
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
    except IndexError: # nothing to parse
        return ""
    except ValueError: # human-readable number
        hours, offset = get_human_readable(input_string, "h")
        minutes, offset = get_human_readable(input_string, "m", offset)
        seconds, offset = get_human_readable(input_string, "s", offset)

    if hours == 0:
        return '{}:{:02}'.format(minutes, seconds)
    return '{}:{:02}:{:02}'.format(hours, minutes, seconds)

replacers = [
    {
        "regex": re.compile(r"(?:(?:https?:)?\/\/)?(?:(?:www|m)\.)?(?:(?:youtube(?:-nocookie)?\.com|youtu.be))(?:\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]+)(\S+)?", re_flags),
        "becomes": "https://y.outube.duckdns.org/{}",
        "timestamp": youtube_timestamp
    },
    {
        "regex": re.compile(r"(?:https?:\/\/)?(?:www\.)?twitter\.com\/(?:#!\/)?(.*)\/status(?:es)?\/([^\/\?\s]+)", re_flags),
        "becomes": "https://fxtwitter.com/{}/status/{}",
    },
    {
        "regex": re.compile(r"(?:https?:\/\/)?(?:www\.)?x\.com\/(?:#!\/)?(.*)\/status(?:es)?\/([^\/\?\s]+)", re_flags),
        "becomes": "https://fixupx.com/{}/status/{}",
    },
    {
        "regex": re.compile(r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/((?:reel)|p)\/([A-Za-z0-9_]{11})[\/\?\w=&]*", re_flags),
        "becomes": "https://ddinstagram.com/{}/{}",
    },
    {
        "regex": re.compile(r"(?:https?:\/\/)?(?:(?:www)|(?:vm))?\.?tiktok\.com\/(@[\w]+)\/?(?:video)?\/?(\d+)?[\S]", re_flags),
        "becomes": "https://tnktok.com/{}/{}",
    },
    {
        "regex": re.compile(r"(?:https?:\/\/)?(?:(?:www)|(?:vm))?\.?tiktok\.com\/([\w]+)\/?", re_flags),
        "becomes": "https://vm.tnktok.com/{}/",
    },
]

link_message = "Da {}[\.]({}) {}"

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
            
            try:
                timestamp = site["timestamp"](r[-1])
            except KeyError:
                timestamp = None

            output.append([link, timestamp])
    return output

async def replace(update: Update, _) -> None:
    try:
        links = parse_text(update.message.text)
    except TypeError:
        links = parse_text(update.message.caption)

    for link in links:
        logger.info(link)

        user = update.effective_user.mention_markdown_v2(update.effective_user.name)
        text = link_message.format(user, link[0], link[1])
        message = await update.effective_chat.send_message(text, parse_mode=ParseMode.MARKDOWN_V2)
        await sleep(FEEDBACK_TIMEOUT)
        await message.edit_reply_markup(reply_markup=get_message_markup())

async def feedback(update: Update, _, data_json: str) -> None:
    data = json.loads(data_json)

    if data["feedback"]:
        await update.callback_query.answer("Bene!")
        await update.effective_message.edit_reply_markup()
        return

    await update.callback_query.answer("Ci ho provato...")
    await update.effective_message.delete()
    return
