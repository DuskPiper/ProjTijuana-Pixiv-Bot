#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Author: DuskPiper

from PixivHelper import PixivHelper
from DBHelper import DBHelper
from Constants import BotMsg
import logging


class BotHandlers:

    @staticmethod
    def start(bot, update):
        bot.sendMessage(
            text=BotMsg.WELCOME,
            chat_id=update.message.chat_id,
            reply_to_message_id=update.message.message_id
        )
        logging.info("New user: " + str(update.message.chat_id))

    @staticmethod
    def help(bot, update):
        bot.sendMessage(
            text=BotMsg.HELP,
            chat_id=update.message.chat_id,
            reply_to_message_id=update.message.message_id
        )

