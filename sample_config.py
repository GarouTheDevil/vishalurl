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
    # Generate screenshots for file after uploading
    # Defaults to True
    SCREENSHOTS = os.environ.get("SCREENSHOTS", "False")
    DEF_THUMB_NAIL_VID_S = os.environ.get("DEF_THUMB_NAIL_VID_S", "")
    # proxy for accessing youtube-dl in GeoRestricted Areas
    # Get your own proxy from https://github.com/rg3/youtube-dl/issues/1091#issuecomment-230163061
    HTTP_PROXY = os.environ.get("HTTP_PROXY", "")
    # https://t.me/hevcbay/951
    OUO_IO_API_KEY = ""
    # maximum message length in Telegram
    MAX_MESSAGE_LENGTH = 4096
    # set timeout for subprocess
    PROCESS_MAX_TIMEOUT = int(os.environ.get("TIME_LIMIT", 0))
    UPROCESS_MAX_TIMEOUT = int(os.environ.get("UTIME_LIMIT", 60))
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

    Bot_username = os.environ.get("Bot_username", "") # Your bot's telegram username (must enter with '@' in the front of the username)
    #If deploying on vps edit the above value as example := Bot_username = "Your-Bot_username-inside-inverted-commas."

    Mega_email = os.environ.get("Mega_email", "None") # This is not necessary! Enter your mega email only if you have a mega.nz account with pro/business features.
    #If deploying on vps edit the above value as example := Mega_email = "Your-Mega_email-inside-inverted-commas."
    
    Mega_password = os.environ.get("Mega_password", "None") # This is not necessary! Enter your mega password only if you have a mega.nz account with pro/business features.
    #If deploying on vps edit the above value as example := Mega_password = "Your-Mega_password-inside-inverted-commas."
    
    REDIS_URI = os.environ.get("REDIS_URI", None) # Get This Value from http://redislabs.com/try-free (If you don't know how to obtain the a video tutorial is available here:- https://t.me/botzupdate/5)
    #If deploying on vps edit the above value as example := REDIS_URI = "Your-Redis-Endpoint-inside-inverted-commas."
    
    REDIS_PASS = os.environ.get("REDIS_PASS", None) # Get This Value from http://redislabs.com/try-free (If you don't know how to obtain the a video tutorial is available here:- https://t.me/botzupdate/5)
    #If deploying on vps edit the above value as example := REDIS_PASS = "Your-Redis-Password-inside-inverted-commas."

    DOWNLOAD_LOCATION = "./DOWNLOADS" # The download location for users. (Don't change anything in this field!)
    ADMIN_LOCATION = "./ADOWNLOADS" # The download location for auth users. (Don't change anything in this field!)
    CREDENTIALS_LOCATION = "./CREDENTIALS" # Location where your mega.nz credentials for megatools gets saved if you provide them. (Don't change anything in this field!)

