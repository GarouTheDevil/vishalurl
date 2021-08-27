import os

class Config(object):
    
    # get a token from @BotFather
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "1479608424:AAFWwiDaPc9md1V1juIEtv7BXeXVbsyi6eY")
    # The Telegram API things
    APP_ID = int(os.environ.get("APP_ID", 1543212))
    API_HASH = os.environ.get("API_HASH", "d47de4b25ddf79a08127b433de32dc84")
    # Get these values from my.telegram.org
    # Array to store users who are authorized to use the bot
    AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "1300445326").split())
    # Banned Unwanted Members..
    BANNED_USERS = set(int(x) for x in os.environ.get("BANNED_USERS", "").split())
    # the download location, where the HTTP Server runs
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    # Telegram maximum file upload size
    MAX_FILE_SIZE = 50000000
    TG_MAX_FILE_SIZE = 2097152000
    FREE_USER_MAX_FILE_SIZE = 50000000
    # chunk size that should be used with requests
    CHUNK_SIZE = 128
    # default thumbnail to be used in the videos
    # default thumbnail to be used in the videos
    DEF_THUMB_NAIL_VID_S = os.environ.get("DEF_THUMB_NAIL_VID_S", "")
    # proxy for accessing youtube-dl in GeoRestricted Areas
    # Get your own proxy from https://github.com/rg3/youtube-dl/issues/1091#issuecomment-230163061
    HTTP_PROXY = os.environ.get("HTTP_PROXY", "")
    # https://t.me/hevcbay/951
    OUO_IO_API_KEY = ""
    # maximum message length in Telegram
    MAX_MESSAGE_LENGTH = 4096
    # set timeout for subprocess
    PROCESS_MAX_TIMEOUT = int(os.environ.get("TIME_LIMIT"))
    # watermark file
    DEF_WATER_MARK_FILE = ""
    # Database url
    DB_URI = os.environ.get("DATABASE_URL", "")
    LOG_CHAN = int(os.environ.get("LOG_CHAN", "-1001145342921"))
    UPDATE_CHANNEL = "DevilBotz"
    DOWNLOADPATH = os.environ.get("DOWNLOADPATH", "Downloads/")
    USERNAME = os.environ.get("USERNAME", "David9010") 
    # dict to hold the ReQuest queue
    ADL_BOT_RQ = {}
