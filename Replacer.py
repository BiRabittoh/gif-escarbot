from telegram import Update
import logging, re
logger = logging.getLogger(__name__)

re_flags = re.I | re.M

replacers = [
    {
        "regex": re.compile(r"(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?", re_flags),
        "becomes": "https://y.outube.duckdns.org/{}"
    },
    {
        "regex": re.compile(r"(?:https?:\/\/)?(?:www\.)?twitter\.com\/(?:#!\/)?(.*)\/status(?:es)?\/([^\/\?\s]+)", re_flags),
        "becomes": "https://fxtwitter.com/{}/status/{}"
    },
]

link_message = "[.]({})"

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
    logger.info(output)
    return output

async def replace(update: Update, _) -> None:
    try:
        links = parse_text(update.message.text)
    except TypeError:
        links = parse_text(update.message.caption)

    for link in links:
        message = link_message.format(link)
        await update.message.reply_text(message, parse_mode="markdown")
