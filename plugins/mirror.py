#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Developed by Spechdie
# Modified by meh 😑 
# (c) Vishal2k2

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from datetime import datetime
import os
import requests
import subprocess
import time
import json
import re

rs = requests.Session()

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from helper_funcs.chat_base import TRChatBase
from helper_funcs.display_progress import progress_for_pyrogram
from pyrogram import Client, Filters, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, UserBannedInChannel


@pyrogram.Client.on_message(pyrogram.Filters.command(["getlink3"]))
async def get_link3(bot, update):
    TRChatBase(update.from_user.id, update.text, "getlink3")
    if str(update.from_user.id) in Config.BANNED_USERS:
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.ABUSIVE_USERS,
            reply_to_message_id=update.message_id,
            disable_web_page_preview=True,
            parse_mode=pyrogram.ParseMode.HTML
        )
        return
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text("🤭 Sorry Dude, You are **B A N N E D 🤣🤣🤣**")
               return
        except UserNotParticipant:
            #await update.reply_text(f"Join @{update_channel} To Use Me")
            await update.reply_text(
                text="**Join My Updates Channel to use ME 😎 🤭**",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="Join My Updates Channel", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        except Exception:
            await update.reply_text("Something Wrong. Contact my Support Group")
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
        except:
            pass
        download_extension = after_download_file_name.rsplit(".", 1)[-1]
        try:
           await bot.edit_message_text(
            text=Translation.SAVED_RECVD_DOC_FILE,
            chat_id=update.chat.id,
            message_id=a.message_id
        )
        except:
            pass
        end_one = datetime.now()
        
        url = "https://up.uploadfiles.io/upload"
        max_days = 30
            
        req = rs.get("https://uploadfiles.io")
        reqdict = req.cookies.get_dict()
        if 'ci_sessions' in reqdict:
                expirykey = reqdict['ci_sessions']
        else:
                await bot.edit_message_text(
                    chat_id=update.chat.id,
                    text="Failed to process the file.",
                    message_id=a.message_id
                )
                return False

        command_to_exec = [
                "curl",
                "--header","Cookie: ci_sessions="+reqdict['ci_sessions']+"; csrf_cookie_name="+reqdict['csrf_cookie_name'],
                "-F", "file=@"+after_download_file_name,
                "-H", "Transfer-Encoding: chunked",
                url
            ]

            # {"status":true,"id":5433363,"url":"https:\/\/ufile.io\/lype2ulr","destination":"https:\/\/uploadfiles.io\/lype2ulr","name":"test.txt","filename":"lype2ulr-test.txt","slug":"lype2ulr","size":"5 Bytes","type":"doc","expiry":"4 Weeks"}
        
        try:
            await a.delete()
        except:
            pass
        try:        
           b = await bot.send_message(
                text=Translation.UPLOAD_START,
                chat_id=update.chat.id,
                reply_to_message_id=update.message_id
            )
        except:
            pass
        try:
                logger.info(command_to_exec)
                t_response = subprocess.check_output(command_to_exec, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
                logger.info("Status : FAIL", exc.returncode, exc.output)
                await bot.edit_message_text(
                    chat_id=update.chat.id,
                    text=exc.output.decode("UTF-8"),
                    message_id=a.message_id
                )
                return False
        else:
                logger.info(t_response)
                print (t_response)

                t_response_arry = json.loads(t_response.decode("UTF-8").split("\n")[-1].strip())['destination']
                
                # scan = re.search(r'.*\"file\"\,[\s\n]*"href":\s*\"(.+)\"', t_response.decode("UTF-8"))
                
                #shorten_api_url = "http://ouo.io/api/{}?s={}".format(Config.OUO_IO_API_KEY, t_response_arry)
                #adfulurl = requests.get(shorten_api_url).text

                rget = rs.get('https://uploadfiles.io/ajax/expiry?hours=168&csrf_test_name='+expirykey)
                print(rget.text)

        try:
            button = [[InlineKeyboardButton("Link 🔗", url=t_response_arry)]]
            markup = InlineKeyboardMarkup(button)
            await bot.edit_message_text(
            chat_id=update.chat.id,
            text=Translation.AFTER_GET_DL_LINK.format(t_response_arry, max_days),
            parse_mode="html",
            reply_markup=markup,
            message_id=b.message_id,
            disable_web_page_preview=True
        )
        except:
            pass
        try:
            os.remove(after_download_file_name)
        except:
            pass
    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text="***Reply to a File to get file mirrored!!***",
            reply_to_message_id=update.message_id
        )
