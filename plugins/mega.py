import os
import logging
import pyrogram
from pyrogram import Filters, Client
from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton
from mega import Mega

from sample_config import Config

# mega client
mega = Mega()
m = mega.login()

# location
LOCATION = "./"

# logging
bot = Client(
   "MegaNz",
   api_id=Config.APP_ID,
   api_hash=Config.API_HASH,
   bot_token=Config.TG_BOT_TOKEN,
)

# mega download
@bot.on_message(filters.regex(pattern="https://mega.nz/") & filters.private)
async def meganz(_, message):
    input = message.text
    user = message.from_user.mention
    msg = await message.reply_text("**Downloading ⬇️**")
    try:
        file = m.download_url(input, LOCATION)
    except Exception as e:
        print(str(e))
        return await msg.edit("**Send Mega Link**")
    await msg.edit("**Uploading ⬆️**")
    cap = f"**Uploaded By** :- {user} \n© @TheAllInOne_Robot"
    await bot.send_document(message.chat.id, file, caption=cap)
    await msg.delete()
    os.remove(file)
