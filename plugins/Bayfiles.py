# (c) Mrvishal2k2
# the logging shits 🤦🏻‍♂️
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# imports 🤷🏻‍♂️
from datetime import datetime
import os
import requests
import subprocess
import time
import json

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this 🚶‍♂️🚶‍♂️
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from helper_funcs.chat_base import TRChatBase
from helper_funcs.display_progress import progress_for_pyrogram
from pyrogram import Client, Filters, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant, UserBannedInChannel

@Client.on_message(Filters.command(["bayupload"]))
async def get_link4(bot, update):
    TRChatBase(update.from_user.id, update.text, "getlink4")
    if str(update.from_user.id) in Config.BANNED_USERS:
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.ABUSIVE_USERS,
            reply_to_message_id=update.message_id,
            disable_web_page_preview=True,
            parse_mode=pyrogram.ParseMode.HTML
        )
        return

    logger.info(update.from_user)
    if update.reply_to_message is not None:
        reply_message = update.reply_to_message
        download_location = Config.DOWNLOAD_LOCATION + "/"
        start = datetime.now()
        a = await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.DOWNLOAD_START,
            reply_to_message_id=update.message_id
        )
        c_time = time.time()
        try:
           after_download_file_name = await bot.download_media(
            message=reply_message,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(Translation.DOWNLOAD_START, a, c_time)
        )
        except Exception as der:
            logger.info(str(der))
            await bot.edit_message_text(
            	  chat_id=update.chat.id,
            	  text=str(der),
            	  message_id=a.message_id
            	  )
            	  
            
        download_extension = after_download_file_name.rsplit(".", 1)[-1]
        try:
           await bot.edit_message_text(
            text=Translation.SAVED_RECVD_DOC_FILE,
            chat_id=update.chat.id,
            message_id=a.message_id
        )
        except:
            pass
            
        try:
            await a.delete()
        except:
            pass
        end_one = datetime.now()
        url = "https://api.bayfiles.com/upload"
        max_days = 5
        command_to_exec = [
                "curl",
                "-F", "file=@"+after_download_file_name,
                url
            ]
            
        try:
           b = await bot.send_message(
                text=Translation.UPLOAD_START,
                chat_id=update.chat.id,
                reply_to_message_id=update.message_id
            )
        except Exception as erro:
            logger.info(str(erro))
            
        try:
            logger.info(command_to_exec)
            t_response = subprocess.check_output(command_to_exec, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
                logger.info("Status : FAIL", exc.returncode, exc.output)
                await bot.edit_message_text(
                    chat_id=update.chat.id,
                    text=exc.output.decode("UTF-8"),
                    message_id=b.message_id
                )
                return False
        else:
                logger.info(t_response)
                print ( t_response )
                t_response_arry = json.loads(t_response.decode("UTF-8").split("\n")[-1].strip())['data']['file']['url']['short']
        try:
            button = [[InlineKeyboardButton("Download Link", url=t_response_arry)]]
            markup = InlineKeyboardMarkup(button)
            await bot.edit_message_text(
            chat_id=update.chat.id,
            text=Translation.AFTER_GET_DL_LINK.format(t_response_arry, max_days),
            parse_mode="html",
            message_id=b.message_id,
            reply_markup=markup,
            disable_web_page_preview=True
        )
        except Exception as e:
            logger.info(str(e))
            
        try:
            os.remove(after_download_file_name)
        except:
            pass
    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text="**Reply To File To Get Link**",
            reply_to_message_id=update.message_id
        )
