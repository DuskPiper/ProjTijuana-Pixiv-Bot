#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Author: DuskPiper
# @Version: 0.1.0

from Constants import *
from BotHandlers import BotHandlers

from os.path import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging


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
updater = Updater(token=token)
dispatcher = updater.dispatcher

# Register handlers
dispatcher.add_handler(CommandHandler("start", BotHandlers.start))
dispatcher.add_handler(CommandHandler("help", BotHandlers.help))
dispatcher.add_handler(CommandHandler("pid", BotHandlers.pid))

# Run bot
updater.start_polling()
logging.info("Pixiv-Bot started...")
updater.bot.sendMessage(
    chat_id=0,
    text='PiperPixivBot backends launched!'
)
