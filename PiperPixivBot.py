#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Author: DuskPiper
# @Version: 0.3.2

from Constants import *
from BotHandlers import BotHandlers

from os.path import *
from telegram.ext import Updater, CommandHandler
import logging


# Config logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

# Load token
token = None
try:
    token_loader = open(join(ROOT_DIR, TOKEN_FILE_NAME), "r")
    token = token_loader.read()
    token_loader.close()
except IOError:
    logging.error("Failed to read token")
    logging.critical("Token file should be in project-dir and named \"{}\"".format(TOKEN_FILE_NAME))
    exit(ExitCode.TOKEN_FILE_NOT_FOUND)

# Initialize bot
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

# Register handlers
dispatcher.add_error_handler(BotHandlers.error_handler)
dispatcher.add_handler(CommandHandler("start", BotHandlers.start))
dispatcher.add_handler(CommandHandler("help", BotHandlers.help))
dispatcher.add_handler(CommandHandler("pid", BotHandlers.pid))
dispatcher.add_handler(CommandHandler("uid", BotHandlers.uid))
dispatcher.add_handler(CommandHandler("downpid", BotHandlers.downpid))

# Run bot
updater.start_polling()
logging.info("Pixiv-Bot started...")
