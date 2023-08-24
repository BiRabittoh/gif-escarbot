import logging
from os import getenv
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

def config_error():
    logger.error("Please create and fill the .env file.")
    exit(1)

try:
    TOKEN = str(getenv("token"))
    GROUP_ID = int(getenv("group_id"))
    CHANNEL_ID = int(getenv("channel_id"))
    ADMIN_ID = int(getenv("admin_id"))
except TypeError:
    config_error()
    
if '' in [TOKEN, GROUP_ID, CHANNEL_ID, ADMIN_ID]:
    config_error()
