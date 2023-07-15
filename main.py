from telegram.ext import MessageHandler, ApplicationBuilder, filters
from telegram import Update
from dotenv import load_dotenv
from os import getenv
import logging

async def forward(update: Update, _):
    if not update.effective_chat.id == int(CHANNEL_ID):
        return logger.info("Ignoring message since it did not come from the correct chat_id.")
    
    if update.channel_post is None:
        return logger.warn("Got an invalid message from the correct chat_id.")
    
    await update.channel_post.forward(GROUP_ID)
    return logger.info("Forwarded a message.")

async def admin_forward(update: Update, _):
    try:
        await update.message.forward(ADMIN_ID)
        return logger.info(f"Forwarded this message to admin: {update.message.text}")
    except:
        return logger.error(f"Couldn't forward this update to admin: {update}")

def config_error():
    logger.error("Please create and fill the .env file.")
    exit(1)

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    load_dotenv()
    
    try:
        TOKEN = str(getenv("token"))
        GROUP_ID = str(getenv("group_id"))
        CHANNEL_ID = str(getenv("channel_id"))
        ADMIN_ID = int(getenv("admin_id"))
    except TypeError:
        config_error()
    
    if '' in [TOKEN, GROUP_ID, CHANNEL_ID, ADMIN_ID]:
        config_error()
    
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, forward))
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE, admin_forward))
    application.run_polling()
