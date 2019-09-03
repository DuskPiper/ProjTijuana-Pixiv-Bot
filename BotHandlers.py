#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Author: DuskPiper

from PixivHelper import PixivHelper
from DBHelper import db
from Constants import *
from PixivArtworks import PixivArtworks

import logging
from re import findall
from telegram.ext import CallbackContext
from telegram.update import Update


class BotHandlers:

    @staticmethod
    def error_handler(update: Update, context: CallbackContext):
        logging.error("An error occurred! Update {} caused {} error.".format(update.update_id, context.error))

    @staticmethod
    def start(update: Update, context: CallbackContext):
        context.bot.send_message(
            text=BotMsg.WELCOME,
            chat_id=update.message.chat_id,
            reply_to_message_id=update.message.message_id
        )
        logging.info("New user: " + str(update.message.chat_id))

    @staticmethod
    def help(update: Update, context: CallbackContext):
        context.bot.send_message(
            text=BotMsg.HELP,
            chat_id=update.message.chat_id,
            reply_to_message_id=update.message.message_id
        )

    @staticmethod
    def pid(update: Update, context: CallbackContext):

        # Validate pid
        if not context.args:
            context.bot.send_message(
                text=BotMsg.WARN_EMPTY_PID,
                chat_id=update.message.chat_id,
                reply_to_message_id=update.message.message_id
            )
            logging.debug("/pid command rejected: lacking args")
            return
        pid = context.args[0]
        if len(context.args) > 1 or "," in pid:
            context.bot.send_message(
                text=BotMsg.WARN_MULTI_PID,
                chat_id=update.message.chat_id,
                reply_to_message_id=update.message.message_id
            )
            logging.debug("/pid command rejected: " + pid)
            return
        pid = "".join(findall(r"\d", pid))
        photo_caption = PIXIV_SHORT_LINK_TEMPLATE.format(pid)

        # Try find image locally, if N/A then call API to download
        artworks_dir = db.search(pid)
        if not artworks_dir:  # not found locally, query API
            artworks: PixivArtworks = PixivHelper.download_artworks_by_pid(pid)
            if not artworks or not artworks.artworks:  # web query failure
                context.bot.send_message(
                    text=BotMsg.ERR_PID_NOT_FOUND,
                    chat_id=update.message.chat_id,
                    reply_to_message_id=update.message.message_id
                )
                logging.debug("/pid command rejected: PID query failure")
                return
            else:  # web query succeed, write to local db
                db.add(artworks)

        # Get image locally
        artworks_dir = db.search(pid)
        if artworks_dir:  # found file locally
            for image_dir in artworks_dir:
                context.bot.send_photo(
                    photo=open(image_dir, "rb"),
                    caption=photo_caption,
                    chat_id=update.message.chat_id
                )
            logging.info("/pid {} success".format(pid))
            return
