from telegram.ext import MessageHandler, ApplicationBuilder, filters
from telegram import Update
import logging, dotenv, os
dotenv.load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def forward(update: Update, _):
    if update.effective_chat.id == CHANNEL_ID:
        if update.channel_post is not None:
            await update.channel_post.forward(GROUP_ID)
            logger.info("Forwarded a message.")

def err_missing_file(filename: str, exit_arg: int = 1):
    
    exit(exit_arg)

if __name__ == "__main__":
    
    try:
        TOKEN = str(os.getenv("token"))
        GROUP_ID = int(os.getenv("group_id"))
        CHANNEL_ID = int(os.getenv("channel_id"))
    except TypeError:
        logger.error(f"Please create and fill the following file: .env")
        exit(1)
    
    if '' in [TOKEN, GROUP_ID, CHANNEL_ID]:
        logger.error(f"Please fill the following file: .env")
        exit(1)
    
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, forward))
    application.run_polling()
