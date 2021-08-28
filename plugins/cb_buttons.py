import os

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from plugins.youtube_dl_button import youtube_dl_call_back
from plugins.dl_button import ddl_call_back
from plugins.help_text import start, help_user
from pyrogram import Client

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
    elif data == "f2v":
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
    elif data == "ghelp":
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
    elif data == "about":
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
    elif data == "start":
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

    if "close" in cb_data:
      await update.message.delete()
    elif "|" in cb_data:
        await youtube_dl_call_back(bot, update)
    elif "=" in cb_data:
        await ddl_call_back(bot, update)
