from telegram import Update
from escarbot.config import CHANNEL_ID, GROUP_ID, ADMIN_ID
import logging
logger = logging.getLogger(__name__)

async def forward(update: Update, _):
    if not update.effective_chat.id == CHANNEL_ID:
        return logger.info("Ignoring message since it did not come from the correct chat_id.")
    
    if update.channel_post is None:
        return logger.warn("Got an invalid message from the correct chat_id.")
    
    await update.channel_post.forward(GROUP_ID)
    return logger.info("Forwarded a message.")

async def admin_forward(update: Update, _):
    try:
        await update.message.forward(ADMIN_ID)
        return logger.info(f"Forwarded this message to admin: { update.message.text }")
    except:
        return logger.error(f"Couldn't forward this update to admin: { update }")
