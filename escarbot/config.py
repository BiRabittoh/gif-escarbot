import logging
from os import getenv
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

INLINE_SEP = 3 * "#"
FEEDBACK_TIMEOUT = int(getenv("feedback_timeout", 3))

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
