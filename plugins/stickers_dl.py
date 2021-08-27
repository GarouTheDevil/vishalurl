# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import time

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)


from helper_funcs.display_progress import progress_for_pyrogram


@pyrogram.Client.on_message(pyrogram.Filters.sticker)
async def DownloadStickersBot(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.BANNED_USER_TEXT,
            reply_to_message_id=update.message_id
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

    #TRChatBase(update.from_user.id, update.text, "stickerdl")
    logger.info(update.from_user)
    download_location = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + "_DownloadStickersBot_" + str(update.from_user.id) + ".png"
    a = await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.DOWNLOAD_START,
        reply_to_message_id=update.message_id
    )
    try:
        c_time = time.time()
        the_real_download_location = await bot.download_media(
            message=update,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(
                Translation.DOWNLOAD_START,
                a,
                c_time
            )
        )
    except (ValueError) as e:
        await bot.edit_message_text(
            text=str(e),
            chat_id=update.chat.id,
            message_id=a.message_id
        )
        return False
    await bot.edit_message_text(
        text=Translation.SAVED_RECVD_DOC_FILE,
        chat_id=update.chat.id,
        message_id=a.message_id
    )
    c_time = time.time()
    await bot.send_document(
        chat_id=update.chat.id,
        document=the_real_download_location,
        # thumb=thumb_image_path,
        # caption=description,
        # reply_markup=reply_markup,
        reply_to_message_id=a.message_id,
        progress=progress_for_pyrogram,
        progress_args=(
            Translation.UPLOAD_START,
            a,
            c_time
        )
    )
    await bot.send_photo(
        chat_id=update.chat.id,
        photo=the_real_download_location,
        # thumb=thumb_image_path,
        # caption=description,
        # reply_markup=reply_markup,
        reply_to_message_id=a.message_id,
        progress=progress_for_pyrogram,
        progress_args=(
            Translation.UPLOAD_START,
            a,
            c_time
        )
    )
    os.remove(the_real_download_location)
    await bot.edit_message_text(
        text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG,
        chat_id=update.chat.id,
        message_id=a.message_id,
        disable_web_page_preview=True
    )
