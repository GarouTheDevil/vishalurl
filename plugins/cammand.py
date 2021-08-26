import pyrogram
from pyrogram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

class Cammand(object):

START_TEXT = """<b>Hi , Iam All In One Bot </b>
"""
    RENAME_403_ERR = "<b>Sorry. Please Rename Again.</b>"
    ABS_TEXT = "<b>Please Don't Be Selfish.</b>"
    # UPGRADE_TEXT = "<b>Please Try Again Or Contact My Master --> @David9010</b>"
    UPGRADE_TEXT = """
**A Modified Multiple Functional Bot**
"""

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('HELP', callback_data='help'),
        InlineKeyboardButton('ABOUT', callback_data='about'),
        InlineKeyboardButton('CLOSE', callback_data='close')
        ]]
    )
    HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('HOME', callback_data='home'),
        InlineKeyboardButton('ABOUT', callback_data='about'),
        InlineKeyboardButton('CLOSE', callback_data='close')
        ]]
    )
    ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('HOME', callback_data='home'),
        InlineKeyboardButton('HELP', callback_data='help'),
        InlineKeyboardButton('CLOSE', callback_data='close')
        ]]
    )
