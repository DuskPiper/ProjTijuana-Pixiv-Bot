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
from telegram import TelegramError, InputMediaPhoto


class BotHandlers:

    @staticmethod
    def error_handler(update: Update, context: CallbackContext):
        logging.error("An error occurred! Update {} caused {} error.".format(
            update.update_id if update else "[Null Updater]",
            context.error
        ))

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
    def uid(update: Update, context: CallbackContext):
        """
        Send recent artworks of uid, image size compressed by telegram
        """

        # Validate uid
        if not context.args:
            context.bot.send_message(
                text=BotMsg.CMD_UID_WARN_EMPTY_UID,
                chat_id=update.message.chat_id,
                reply_to_message_id=update.message.message_id
            )
            logging.debug("/uid command rejected: lacking args")
            return
        uid = context.args[0]
        if len(context.args) > 1 or "," in uid:
            context.bot.send_message(
                text=BotMsg.CMD_UID_WARN_MULTI_UID,
                chat_id=update.message.chat_id,
                reply_to_message_id=update.message.message_id
            )
            logging.debug("/uid command rejected: " + uid)
            return
        uid = "".join(findall(r"\d", uid))

        # Query all PID under UID, then validate result
        all_pid = sorted(PixivHelper.get_all_pid_by_uid(uid), reverse=True)
        if not all_pid:  # not result
            context.bot.send_message(
                text=BotMsg.CMD_UID_ERR_UID_NOT_FOUND,
                chat_id=update.message.chat_id,
                reply_to_message_id=update.message.message_id
            )
            return
        if len(all_pid) > UID_MODE_LIMIT:  # too many results
            context.bot.send_message(
                text=BotMsg.CMD_UID_INFO_LIMIT_REACHED,
                chat_id=update.message.chat_id
            )
            all_pid = all_pid[:UID_MODE_LIMIT]

        # Query and send each PID
        for pid in all_pid:
            artworks_dir = db.search(pid)
            photo_caption = PIXIV_SHORT_LINK_TEMPLATE.format(pid)
            if not artworks_dir:  # not found locally, query API
                artworks: PixivArtworks = PixivHelper.download_artworks_by_pid(pid)
                if not artworks or not artworks.artworks:  # web query failure
                    context.bot.send_message(
                        text=BotMsg.CMD_PID_ERR_PID_NOT_FOUND,
                        chat_id=update.message.chat_id,
                        reply_to_message_id=update.message.message_id
                    )
                    logging.debug("/pid command rejected: PID query failure")
                    continue
                else:  # web query succeed, write to local db
                    db.add(artworks)
            artworks_dir = db.search(pid)
            if artworks_dir:  # found file locally
                for image_dir in artworks_dir:
                    context.bot.send_photo(
                        photo=open(image_dir, "rb"),
                        caption=photo_caption,
                        chat_id=update.message.chat_id
                    )
        logging.info("/uid {} success".format(uid))

    @staticmethod
    def downpid(update: Update, context: CallbackContext):
        """
        Download by pid, send original sized image file by pid
        """

        # Validate pid
        if not context.args:
            context.bot.send_message(
                text=BotMsg.CMD_PID_WARN_EMPTY_PID,
                chat_id=update.message.chat_id,
                reply_to_message_id=update.message.message_id
            )
            logging.debug("/pid command rejected: lacking args")
            return
        pid = context.args[0]
        if len(context.args) > 1 or "," in pid:
            context.bot.send_message(
                text=BotMsg.CMD_PID_WARN_MULTI_PID,
                chat_id=update.message.chat_id,
                reply_to_message_id=update.message.message_id
            )
            logging.debug("/pid command rejected: " + pid)
            return
        pid = "".join(findall(r"\d", pid))

        print(">>> CMD /downpid", pid)
        # Try find image locally, if N/A then call API to download
        artworks_dir = db.search(pid)
        if not artworks_dir:  # not found locally, query API
            artworks: PixivArtworks = PixivHelper.download_artworks_by_pid(pid)
            if not artworks or not artworks.artworks:  # web query failure
                context.bot.send_message(
                    text=BotMsg.CMD_PID_ERR_PID_NOT_FOUND,
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
                try:
                    context.bot.send_document(
                        document=open(image_dir, "rb"),
                        chat_id=update.message.chat_id
                    )
                except TelegramError:
                    context.bot.send_message(
                        text=BotMsg.CMD_DOWNPID_ERR_FAIL_TO_SEND,
                        chat_id=update.message.chat_id
                    )
            logging.info("/pid {} success".format(pid))
            return

    @staticmethod
    def pid(update: Update, context: CallbackContext):
        """
        Send artworks of pid, image size compressed by telegram
        """

        # Validate pid
        if not context.args:
            context.bot.send_message(
                text=BotMsg.CMD_PID_WARN_EMPTY_PID,
                chat_id=update.message.chat_id,
                reply_to_message_id=update.message.message_id
            )
            logging.debug("/pid command rejected: lacking args")
            return
        pid = context.args[0]
        if len(context.args) > 1 or "," in pid:
            context.bot.send_message(
                text=BotMsg.CMD_PID_WARN_MULTI_PID,
                chat_id=update.message.chat_id,
                reply_to_message_id=update.message.message_id
            )
            logging.debug("/pid command rejected: " + pid)
            return
        pid = "".join(findall(r"\d", pid))
        # photo_caption = PIXIV_SHORT_LINK_TEMPLATE.format(pid)

        # Try find image locally, if N/A then call API to download
        artworks_dir = db.search(pid)
        if not artworks_dir:  # not found locally, query API
            artworks: PixivArtworks = PixivHelper.download_artworks_by_pid(pid)
            if not artworks or not artworks.artworks:  # web query failure
                context.bot.send_message(
                    text=BotMsg.CMD_PID_ERR_PID_NOT_FOUND,
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
            image_group = []
            for image_dir in artworks_dir:
                image_group.append(InputMediaPhoto(open(image_dir, "rb")))
            context.bot.send_media_group(
                chat_id=update.message.chat_id,
                media=image_group
            )
            logging.info("/pid {} success".format(pid))
            return

    @staticmethod
    def search(query, page=1, per_page=30, mode="text",
               period="all", order="desc", sort="date",
               types=("illustration", "manga", "ugoira"),
               image_sizes=("px_128x128", "large"),
               include_stats=True, include_sanity_level=True):
        params = {
            "q": query,
            "page": page,
            "per_page": per_page,
            "period": period,
            "order": order,
            "sort": sort,
            "mode": mode,
            "types": ",".join(types),
            "include_stats": include_stats,
            "include_sanity_level": include_sanity_level,
            "image_sizes": ",".join(image_sizes),
        }
