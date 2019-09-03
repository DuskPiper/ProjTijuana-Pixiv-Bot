#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Author: DuskPiper

from os.path import *
from Constants import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from DBHelper import DBHelper


token = None
try:
    token_loader = open(join(ROOT_DIR, TOKEN_FILE_NAME), "r")
    token = token_loader.read()
    token_loader.close()
except IOError:
    logging.error("Failed to read token")
    logging.critical("Token file should be in project-dir and named \"{}\"".format(TOKEN_FILE_NAME))
    exit(ExitCode.TOKEN_FILE_NOT_FOUND)

DB = DBHelper()
updater = Updater(token=token)
dispatcher = updater.dispatcher
