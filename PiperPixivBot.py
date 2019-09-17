#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Author: DuskPiper
# @Version: 0.5.4

from Constants import *
from BotHandlers import BotHandlers

from os.path import *
from telegram.ext import Updater, CommandHandler


# Load telegram-bot token
token = None
try:
    token_loader = open(join(ROOT_DIR, TOKEN_FILE_NAME), "r")
    token = token_loader.read()
    token_loader.close()
    LOGGER.info("Token loaded")
except IOError:
    LOGGER.error("Failed to load token")
    LOGGER.error("Token file should be in project-dir and named \"{}\"".format(TOKEN_FILE_NAME))
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
dispatcher.add_handler(CommandHandler("search", BotHandlers.search))
dispatcher.add_handler(CommandHandler("erosearch", BotHandlers.eroSearch))
dispatcher.add_handler(CommandHandler("remilia", BotHandlers.remilia))

# Run bot
updater.start_polling()
LOGGER.info("Pixiv-Bot started...")
