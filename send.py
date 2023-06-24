from dotenv import load_dotenv
from os import getenv
load_dotenv()

## Config start
endpoint = "sendMessage"
payload = {
    "chat_id": getenv("group_id"),
    "text": "Hello world!",
    
    "parse_mode": "markdown",
    "reply_to_message_id": None,
    "disable_web_page_preview": False,
    "disable_notification": False,
}
## Config end

from requests import post
response = post(f"https://api.telegram.org/bot{getenv('token')}/{endpoint}", json=payload,
                headers={ "accept": "application/json", "content-type": "application/json" })
print(response.text)
