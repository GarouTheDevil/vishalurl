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
from plugins.dl_button import ddl_call_back

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation


@DevilBotz.on_message(pyrogram.Filters.command(["help"]))
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
            await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_USER,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Rename', callback_data = "rename"),
                    InlineKeyboardButton('File To Video', callback_data = "f2v")
                ],
                [
                    InlineKeyboardButton('Thumbnail', callback_data = "customthumb"),
                    InlineKeyboardButton('File To Link', callback_data = "f2l")
                ],
                [
                    InlineKeyboardButton('File To File', callback_data = "f2f"),
                    InlineKeyboardButton('Trim', callback_data = "trim")
                ],
                [
                    InlineKeyboardButton('Url Uploading', callback_data = "urlupload"),
                    InlineKeyboardButton('ABOUT', callback_data = "about")
                ],
                [
                    InlineKeyboardButton('BACK', callback_data = "cthumb")
                ]
            ]
        )
    )       

@DevilBotz.on_message(pyrogram.Filters.command(["start"]))
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
            return 

@DevilBotz.on_callback_query()
async def cb_handler(client: DevilBotz , query: CallbackQuery):
    data = query.data
        if data == "rename":
        await query.message.edit_text(
            text=Translation.INLINE_RENAME,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Back', callback_data = "ghelp"),
                    InlineKeyboardButton("CLOSE", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "c2v":
        await query.message.edit_text(
            text=Translation.INLINE_C2V,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Back', callback_data = "ghelp"),
                    InlineKeyboardButton("CLOSE", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "customthumb":
        await query.message.edit_text(
            text=Translation.INLINE_THUMB,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Back', callback_data = "ghelp"),
                    InlineKeyboardButton("CLOSE", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "f2l":
        await query.message.edit_text(
            text=Translation.INLINE_F2L,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Back', callback_data = "ghelp"),
                    InlineKeyboardButton("CLOSE", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "f2f":
        await query.message.edit_text(
            text=Translation.INLINE_F2F,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Back', callback_data = "ghelp"),
                    InlineKeyboardButton("CLOSE", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "trim":
        await query.message.edit_text(
            text=Translation.INLINE_TRIM,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Back', callback_data = "ghelp"),
                    InlineKeyboardButton("CLOSE", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "urlupload":
        await query.message.edit_text(
            text=Translation.INLINE_URLUPLOAD,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Back', callback_data = "ghelp"),
                    InlineKeyboardButton("CLOSE", callback_data = "close")
                ]
            ]
        )
     )
    elif "ghelp" in cb_data:
        await query.message.edit_text(
            text=Translation.HELP_USER,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Rename', callback_data = "rename"),
                    InlineKeyboardButton('File To Video', callback_data = "f2v")
                ],
                [
                    InlineKeyboardButton('Thumbnail', callback_data = "customthumb"),
                    InlineKeyboardButton('File To Link', callback_data = "f2l")
                ],
                [
                    InlineKeyboardButton('File To File', callback_data = "f2f"),
                    InlineKeyboardButton('Trim', callback_data = "trim")
                ],
                [
                    InlineKeyboardButton('Url Uploading', callback_data = "urlupload"),
                    InlineKeyboardButton('ABOUT', callback_data = "about")
                ],
                [
                    InlineKeyboardButton('BACK', callback_data = "cthumb")
                ]
            ]
        )
    )       
    elif "about" in cb_data:
        await query.message.edit_text(
            text=Translation.UPGRADE_TEXT,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Back', callback_data = "ghelp"),
                    InlineKeyboardButton("CLOSE", callback_data = "close")
                ]
            ]
        )
     )
    elif "start" in cb_data:
        await query.message.edit_text(
            text=Transition.START_TEXT,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup (
            [
                [
                        InlineKeyboardButton("HELP", callback_data = "ghelp"),
                        InlineKeyboardButton("ABOUT", callback_data = "about"),
                        InlineKeyboardButton("CLOSE", callback_data = "close")
                ]
            ]
        )
     )   
     elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
