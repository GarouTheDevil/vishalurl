import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import os
import re
import json
import math
import time
import shutil
import random
import ffmpeg
import asyncio
import requests

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from translation import Translation

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, UserBannedInChannel
from database.database import *
from helper_funcs.display_progress import humanbytes
from helper_funcs.help_uploadbot import DownLoadFile

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from datetime import datetime
from PIL import Image

@Client.on_message(filters.private & filters.regex(pattern=".*http.*"))
async def echo(bot, update):
    if "youtu" not in update.text:
        await bot.edit_message_text(chat_id=update.chat.id, text=Translation.BLOCK_LIST_TEXT, disable_web_page_preview=True, parse_mode="html", message_id=fmsg.message_id)
        return
    logger.info(update.from_user.id)
    fmsg = await update.reply_text(text=Translation.CHECKING_LINK, quote=True)
    url = update.text
    if Config.UPDATE_CHANNEL:
        try:
            user = await bot.get_chat_member(Config.UPDATE_CHANNEL, update.chat.id)
            if user.status == "kicked":
              await bot.edit_message_text(text=Translation.BANNED_USER_TEXT, message_id=fmsg.message_id)
              return
        except UserNotParticipant:
            await bot.edit_message_text(chat_id=update.chat.id, text=Translation.FORCE_SUBSCRIBE_TEXT, message_id=fmsg.message_id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Join Channel", url=f"https://telegram.me/{Config.UPDATE_CHANNEL}")]]))
            return
        except Exception:
            await bot.edit_message_text(chat_id=update.chat.id, text=Translation.SOMETHING_WRONG, message_id=fmsg.message_id)
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
                await bot.edit_message_text(chat_id=update.chat.id, text=Translation.FREE_USER_LIMIT_Q_SZE.format(process_max_timeout, present_time), disable_web_page_preview=True, parse_mode="html", message_id=fmsg.message_id)
                return
        else:
            Config.ADL_BOT_RQ[str(update.from_user.id)] = time.time()
    youtube_dl_username = None
    youtube_dl_password = None
    file_name = None
    if "|" in url:
        url_parts = url.split("|")
        if len(url_parts) == 2:
            url = url_parts[0]
            file_name = url_parts[1]
        elif len(url_parts) == 4:
            url = url_parts[0]
            file_name = url_parts[1]
            youtube_dl_username = url_parts[2]
            youtube_dl_password = url_parts[3]
        else:
            for entity in update.entities:
                if entity.type == "text_link":
                    url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    l = entity.length
                    url = url[o:o + l]
        if url is not None:
            url = url.strip()
        if file_name is not None:
            file_name = file_name.strip()
        if youtube_dl_username is not None:
            youtube_dl_username = youtube_dl_username.strip()
        if youtube_dl_password is not None:
            youtube_dl_password = youtube_dl_password.strip()
        logger.info(url)
        logger.info(file_name)
    else:
        for entity in update.entities:
            if entity.type == "text_link":
                url = entity.url
            elif entity.type == "url":
                o = entity.offset
                l = entity.length
                url = url[o:o + l]
    if Config.HTTP_PROXY != "":
        command_to_exec = [
            "youtube-dl",
            "--no-warnings",
            "--youtube-skip-dash-manifest",
            "-j",
            url,
            "--proxy", Config.HTTP_PROXY
        ]
    else:
        command_to_exec = [
            "youtube-dl",
            "--no-warnings",
            "--youtube-skip-dash-manifest",
            "-j",
            url
        ]
    if "hotstar" in url:
        command_to_exec.append("--geo-bypass-country")
        command_to_exec.append("IN")
    if youtube_dl_username is not None:
        command_to_exec.append("--username")
        command_to_exec.append(youtube_dl_username)
    if youtube_dl_password is not None:
        command_to_exec.append("--password")
        command_to_exec.append(youtube_dl_password)
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    # logger.info(e_response)
    t_response = stdout.decode().strip()
    # logger.info(t_response)

    if e_response and "nonnumeric port" not in e_response:
        # logger.warn("Status : FAIL", exc.returncode, exc.output)
        error_message = e_response.replace("please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output.", "")
        if "This video is only available for registered users." in error_message:
            error_message += Translation.SET_CUSTOM_USERNAME_PASSWORD
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.NO_VOID_FORMAT_FOUND.format(str(error_message)),
            reply_to_message_id=update.message_id,
            parse_mode="html",
            disable_web_page_preview=True
        )
        return False
    if t_response:
        x_reponse = t_response
        if "\n" in x_reponse:
            x_reponse, _ = x_reponse.split("\n")
        response_json = json.loads(x_reponse)
        save_ytdl_json_path = Config.DOWNLOAD_LOCATION + \
            "/" + str(update.from_user.id) + ".json"
        with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
            json.dump(response_json, outfile, ensure_ascii=False)
        # logger.info(response_json)
        inline_keyboard = []
        duration = None
        if "duration" in response_json:
            duration = response_json["duration"]
        if "formats" in response_json:
            for formats in response_json["formats"]:
                format_id = formats.get("format_id")
                format_string = formats.get("format_note")
                if format_string is None:
                    format_string = formats.get("format")
                format_ext = formats.get("ext")
                approx_file_size = ""
                if "filesize" in formats:
                    approx_file_size = humanbytes(formats["filesize"])
                cb_string_video = "{}|{}|{}".format(
                    "video", format_id, format_ext)
                cb_string_file = "{}|{}|{}".format(
                    "file", format_id, format_ext)
                if format_string is not None and not "audio only" in format_string:
                    ikeyboard = [
                        InlineKeyboardButton(
                            "Streamable Video " + format_string + " video " + approx_file_size + " ",
                            callback_data=(cb_string_video).encode("UTF-8")
                        ),
                        InlineKeyboardButton(
                            "Downloadble File " + format_ext + " " + approx_file_size + " ",
                            callback_data=(cb_string_file).encode("UTF-8")
                        )
                    ]
                    """if duration is not None:
                        cb_string_video_message = "{}|{}|{}".format(
                            "vm", format_id, format_ext)
                        ikeyboard.append(
                            InlineKeyboardButton(
                                "VM",
                                callback_data=(
                                    cb_string_video_message).encode("UTF-8")
                            )
                        )"""
                else:
                    ikeyboard = [
                        InlineKeyboardButton(
                            "Streamable Video [" +
                            "] ( " +
                            approx_file_size + " )",
                            callback_data=(cb_string_video).encode("UTF-8")
                        ),
                        InlineKeyboardButton(
                            "Downloadble File [" +
                            "] ( " +
                            approx_file_size + " )",
                            callback_data=(cb_string_file).encode("UTF-8")
                        )
                    ]
                inline_keyboard.append(ikeyboard)
            if duration is not None:
                cb_string_64 = "{}|{}|{}".format("audio", "64k", "mp3")
                cb_string_128 = "{}|{}|{}".format("audio", "128k", "mp3")
                cb_string = "{}|{}|{}".format("audio", "320k", "mp3")
                inline_keyboard.append([
                    InlineKeyboardButton(
                        "MP3" + "(" + "64 kbps" + ")", callback_data=cb_string_64.encode("UTF-8")),
                    InlineKeyboardButton(
                        "MP3" + "(" + "128 kbps" + ")", callback_data=cb_string_128.encode("UTF-8"))
                ])
                inline_keyboard.append([
                    InlineKeyboardButton(
                        "Mp3" + "(" + "320 kbps" + ")", callback_data=cb_string.encode("UTF-8"))
                ])
        else:
            format_id = response_json["format_id"]
            format_ext = response_json["ext"]
            cb_string_file = "{}|{}|{}".format(
                "file", format_id, format_ext)
            cb_string_video = "{}|{}|{}".format(
                "video", format_id, format_ext)
            inline_keyboard.append([
                InlineKeyboardButton(
                    "Streamable Video",
                    callback_data=(cb_string_video).encode("UTF-8")
                ),
                InlineKeyboardButton(
                    "Downloadable File",
                    callback_data=(cb_string_file).encode("UTF-8")
                )
            ])
            cb_string_file = "{}={}={}".format(
                "file", format_id, format_ext)
            cb_string_video = "{}={}={}".format(
                "video", format_id, format_ext)
            inline_keyboard.append([
                InlineKeyboardButton(
                    "video",
                    callback_data=(cb_string_video).encode("UTF-8")
                ),
                InlineKeyboardButton(
                    "file",
                    callback_data=(cb_string_file).encode("UTF-8")
                )
            ])
        reply_markup = InlineKeyboardMarkup(inline_keyboard)

        thumbnail = Config.DEF_THUMB_NAIL_VID_S
        thumbnail_image = Config.DEF_THUMB_NAIL_VID_S
        thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"

        if not os.path.exists(thumb_image_path):
            mes = await thumb(update.from_user.id)
            if mes != None:
                m = await bot.get_messages(update.chat.id, mes.msg_id)
                await m.download(file_name=thumb_image_path)
                thumb_image_path = thumb_image_path
            else:
                if "thumbnail" in response_json:
                    if response_json["thumbnail"] is not None:
                        thumbnail = response_json["thumbnail"]
                        thumbnail_image = response_json["thumbnail"]
                thumb_image_path = DownLoadFile(
                    thumbnail_image,
                    Config.DOWNLOAD_LOCATION + "/" +
                    str(update.from_user.id) + ".jpg",
                    Config.CHUNK_SIZE,
                    None,  # bot,
                    Translation.DOWNLOAD_START,
                    update.message_id,
                    update.chat.id
                )
        await fmsg.delete()
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.FORMAT_SELECTION.format(thumbnail) + "\n\n" + Translation.SET_CUSTOM_USERNAME_PASSWORD,
            reply_markup=reply_markup,
            parse_mode="html",
            reply_to_message_id=update.message_id
        )
    else:
        inline_keyboard = []
        cb_string_file = "{}={}={}".format(
            "file", "LFO", "NONE")
        cb_string_video = "{}={}={}".format(
            "video", "OFL", "ENON")
        inline_keyboard.append([
            InlineKeyboardButton(
                "SVideo",
                callback_data=(cb_string_video).encode("UTF-8")
            ),
            InlineKeyboardButton(
                "DFile",
                callback_data=(cb_string_file).encode("UTF-8")
            )
        ])
        reply_markup = InlineKeyboardMarkup(inline_keyboard)

        await intmsg.delete()
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.FORMAT_SELECTION.format(""),
            reply_markup=reply_markup,
            parse_mode="html",
            reply_to_message_id=update.message_id
        )
