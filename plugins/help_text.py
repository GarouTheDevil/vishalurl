import os
import sqlite3
from pyrogram import (
    Client,
    Filters,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

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
