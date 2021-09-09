import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import pyrogram
import os
import sqlite3
from pyrogram import Filters
from pyrogram import Client
from pyrogram import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from pyrogram.errors import UserNotParticipant, UserBannedInChannel 

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation


@Client.on_message(pyrogram.Filters.command(["help"]))
async def help_user(bot, update):
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text("**Your Banned**")
               return
        except UserNotParticipant:
            await update.reply_text(
                text="**Join Updates Channel**",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="Join Updates Channel", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        else:
            await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_USER,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Rename File', callback_data = "rename"),
                    InlineKeyboardButton('Rename Video', callback_data = "renamevid")
                ],
                [
                    InlineKeyboardButton('File To Video', callback_data = "f2v"),
                    InlineKeyboardButton('File To Link', callback_data = "f2l")
                ],
                [
                    InlineKeyboardButton('Trim', callback_data = "trim"),
                    InlineKeyboardButton('File To File', callback_data = "f2f")
                ],
                [
                    InlineKeyboardButton('Url Uploading', callback_data = "urlupload"),
                    InlineKeyboardButton('Thumbnail', callback_data = "cthumb")
                ],
                [
                    InlineKeyboardButton('BACK', callback_data = "ghelp"),
                    InlineKeyboardButton('ABOUT', callback_data = "about")
                ]
            ]
        )
    )       

@Client.on_message(pyrogram.Filters.command(["start"]))
async def start(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await update.reply_text("You are Banned")
        return
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text("**Your Banned**")
               return
        except UserNotParticipant:
            #await update.reply_text(f"Join Updates Channel")
            await update.reply_text(
                text="**Join Update Channel**",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="Join My Updates Channel", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        else:
            await update.reply_text(Translation.START_TEXT.format(update.from_user.first_name),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton("HELP", callback_data = "ghelp"),
                        InlineKeyboardButton("ABOUT", callback_data = "about"),
                        InlineKeyboardButton("CLOSE", callback_data = "close")
                ]
            ]
        ),
        reply_to_message_id=update.message_id
    )
@Client.on_message(pyrogram.Filters.command(["about"]))
async def about(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await update.reply_text("You are Banned")
        return
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text("**Your Banned**")
               return
        except UserNotParticipant:
            #await update.reply_text(f"Join Updates Channel")
            await update.reply_text(
                text="**Join Update Channel**",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="Join My Updates Channel", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        else:
            await update.reply_text(Translation.UPGRADE_TEXT.format(update.from_user.first_name),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton("START", callback_data = "start"),
                        InlineKeyboardButton("HELP", callback_data = "ghelp"),
                        InlineKeyboardButton("CLOSE", callback_data = "close")
                ]
            ]
        ),
        reply_to_message_id=update.message_id
    )


