#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Ns_AnoNymouS 
# Edit by MrVishal2k2

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import time
import random
# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

PROCESS_MAX_TIMEOUT = int(os.environ.get("TIME_LIMIT"))
ADL_BOT_RQ = {}

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram import Client, Filters
from helper_funcs.help_Nekmo_ffmpeg import take_screen_shot

from helper_funcs.display_progress import progress_for_pyrogram

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from datetime import datetime

# https://stackoverflow.com/a/37631799/4723940
from PIL import Image
from database.database import *
from pyrogram import Client, Filters, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, UserBannedInChannel

@pyrogram.Client.on_message(pyrogram.Filters.command(["rename_video"]))
async def rename_video(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
        return
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text("**Your Banned**")
               return
        except UserNotParticipant:
            #await update.reply_text(f"Join @{update_channel} To Use Me")
            await update.reply_text(
                text="**Join Channel**",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="Join My Updates Channel", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        except Exception:
            await update.reply_text("Something Wrong. Contact my Support Group")
            return

    if update.from_user.id not in Config.AUTH_USERS:
        # restrict free users from sending more links
        if str(update.from_user.id) in Config.ADL_BOT_RQ:
            current_time = time.time()
            previous_time = Config.ADL_BOT_RQ[str(update.from_user.id)]
            process_max_timeout = round(Config.PROCESS_MAX_TIMEOUT/60)
            present_time = round(Config.PROCESS_MAX_TIMEOUT-(current_time - previous_time))
            Config.ADL_BOT_RQ[str(update.from_user.id)] = time.time()
            if round(current_time - previous_time) < Config.PROCESS_MAX_TIMEOUT:
                await bot.send_message(
                    chat_id=update.chat.id,
                    text=f"<b>To Avoid Weight On Bot , 1 Request Per {process_max_timeout} Minute. \nPlease Try Again After {present_time} Seconds.</b>",
                    disable_web_page_preview=True,
                    parse_mode="html",
                    reply_to_message_id=update.message_id
                )
                return
        else:
            Config.ADL_BOT_RQ[str(update.from_user.id)] = time.time()

    #TRChatBase(update.from_user.id, update.text, "rename_video")
    if (" " in update.text) and (update.reply_to_message is not None):
        cmd, file_name = update.text.split(" ", 1)
        if len(file_name) > 64:
            await update.reply_text(
                Translation.IFLONG_FILE_NAME.format(
                    alimit="64",
                    num=len(file_name)
                )
            )
            return
        description = Translation.CUSTOM_CAPTION_UL_FILE
        download_location = Config.DOWNLOAD_LOCATION + "/"
        b = await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.DOWNLOAD_START,
            reply_to_message_id=update.message_id
        )
        c_time = time.time()
        try:
           the_real_download_location = await bot.download_media(
            message=update.reply_to_message,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(
                Translation.DOWNLOAD_START,
                b,
                c_time
            )
        )
        except:
            pass
        if the_real_download_location is not None:
            try:
                await bot.edit_message_text(
                    text=Translation.SAVED_RECVD_DOC_FILE,
                    chat_id=update.chat.id,
                    message_id=b.message_id
                )
            except:
                pass
            new_file_name = download_location + file_name
            os.rename(the_real_download_location, new_file_name)
            await bot.edit_message_text(
                text=Translation.UPLOAD_START,
                chat_id=update.chat.id,
                message_id=b.message_id
                )
            logger.info(the_real_download_location)
            width = 0
            height = 0
            duration = 0
            metadata = extractMetadata(createParser(new_file_name))
            try:
             if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            except:
              pass
            thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
            if not os.path.exists(thumb_image_path):
                mes = await thumb(update.from_user.id)
                if mes != None:
                    m = await bot.get_messages(update.chat.id, mes.msg_id)
                    await m.download(file_name=thumb_image_path)
                    thumb_image_path = thumb_image_path
                else:
                    thumb_image_path = await take_screen_shot(new_file_name, os.path.dirname(new_file_name), random.randint(0, duration - 1))
            else:
                width = 0
                height = 0
                metadata = extractMetadata(createParser(thumb_image_path))
                if metadata.has("width"):
                    width = metadata.get("width")
                if metadata.has("height"):
                    height = metadata.get("height")
                # resize image
                # ref: https://t.me/PyrogramChat/44663
                # https://stackoverflow.com/a/21669827/4723940
                Image.open(thumb_image_path).convert("RGB").save(thumb_image_path)
                img = Image.open(thumb_image_path)
                # https://stackoverflow.com/a/37631799/4723940
                # img.thumbnail((90, 90))
                img.resize((320, height))
                img.save(thumb_image_path, "JPEG")
                # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
            c_time = time.time()
            await bot.send_video(
                chat_id=update.chat.id,
                video=new_file_name,
                duration=duration,
                thumb=thumb_image_path,
                caption=f"<b>{file_name}</b>",
                # reply_markup=reply_markup,
                reply_to_message_id=update.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    Translation.UPLOAD_START,
                    b, 
                    c_time
                )
            )
            try:
                os.remove(new_file_name)
                os.remove(thumb_image_path)
            except:
                pass
            await bot.edit_message_text(
                text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG,
                chat_id=update.chat.id,
                message_id=b.message_id,
                disable_web_page_preview=True
            )
    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.REPLY_TO_DOC_FOR_RENAME_FILE,
            reply_to_message_id=update.message_id
        )
