import os

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from plugins.youtube_dl_button import youtube_dl_call_back
from plugins.dl_button import ddl_call_back
from pyrogram import Client
from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.help_text import help_user, start

@Client.on_callback_query()
async def button(bot, update):
    if "|" in update.data:
        await youtube_dl_call_back(bot, update)
    elif "=" in update.data:
        await ddl_call_back(bot, update)
    elif update.data == "start":
        await update.message.edit_text(
            text=Translation.START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton("HELP", callback_data = "ghelp"),
                        InlineKeyboardButton("ABOUT", callback_data = "about"),
                        InlineKeyboardButton("CLOSE", callback_data = "close")
                ]
            ]
        ))
    elif update.data == "ghelp":
        await update.message.edit_text(
            text=Translation.HELP_TEXT,
            disable_web_page_preview=True,
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
        ))
    elif update.data == "rename":
       await update.message.edit.text(
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
    elif update.data == "c2v":
       await update.message.edit.text(
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
    elif update.data == "customthumb":
       await update.message.edit.text(
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
    elif update.data == "f2l":
       await update.message.edit.text(
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
    elif update.data == "f2f":
       await update.message.edit.text(
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
    elif update.data == "trim":
       await update.message.edit.text(
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
    elif update.data == "urlupload":
       await update.message.edit.text(
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
    elif update.data == "ghelp":
       await update.message.edit.text(
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
    elif update.data == "about":
       await update.message.edit.text(
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
    elif update.data == "start":
       await update.message.edit.text(
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
        await update.message.delete()
        try:
            await update.message.reply_to_message.delete()
        except:
            pass
   
