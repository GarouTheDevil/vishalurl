#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import json
import math
import os
import shutil
import subprocess
import time
from pyrogram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from helper_funcs.chat_base import TRChatBase
from helper_funcs.display_progress import progress_for_pyrogram, humanbytes
from plugins.youtube_dl_button import youtube_dl_call_back
from plugins.dl_button import ddl_call_back
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from plugins.help_text import start, about_meh, upgrade, help_user
from PIL import Image

@pyrogram.Client.on_callback_query()
async def button(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.message.chat.id,
            message_ids=update.message.message_id,
            revoke=True
        )
        return
    # logger.info(update)
    cb_data = update.data
    
    if "home" in cb_data:
        test0 = [[
               InlineKeyboardButton("ABOUT", callback_data="about"),
               InlineKeyboardButton("HELP", callback_data="help"),
                InlineKeyboardButton("CLOSE", callback_data="closeme"),
                ]]
        mark0 = InlineKeyboardMarkup(test0)

        await update.message.delete()
        await bot.send_message(chat_id=update.message.chat.id, text=Translation.START_TEXT, disable_web_page_preview=True, reply_to_message_id=update.message.reply_to_message.message_id, reply_markup=mark0)

    if "about" in cb_data:
        test1 = [[
               InlineKeyboardButton("START", callback_data="home"),
               InlineKeyboardButton("HELP", callback_data="help"),
               InlineKeyboardButton("CLOSE", callback_data="closeme"),
                ]]
        mark1 = InlineKeyboardMarkup(test1)

        await update.message.delete()
        await bot.send_message(chat_id=update.message.chat.id, text=Translation.UPGRADE_TEXT, disable_web_page_preview=True, reply_to_message_id=update.message.reply_to_message.message_id, reply_markup=mark1)

    if "help" in cb_data:
        test2 = [[
               InlineKeyboardButton("START", callback_data="home"),
               InlineKeyboardButton("ABOUT", callback_data="about"),
               InlineKeyboardButton("CLOSE", callback_data="closeme"),
                ]]
        mark2 = InlineKeyboardMarkup(test2)

        await update.message.delete()
        await bot.send_message(chat_id=update.message.chat.id, text=Translation.HELP_USER, disable_web_page_preview=True, reply_to_message_id=update.message.reply_to_message.message_id, reply_markup=mark2)

    if "closeme" in cb_data:
      await update.message.delete()

    elif "|" in cb_data:
        await youtube_dl_call_back(bot, update)
    elif "=" in cb_data:
        await ddl_call_back(bot, update)

@pyrogram.Client.on_callback_query()
async def formatbuttons(bot, update):
       
    if "|" in update.data:
        await zee5_execute(bot, update)
        
    elif "closeformat" in update.data:     
        await update.message.delete() 
