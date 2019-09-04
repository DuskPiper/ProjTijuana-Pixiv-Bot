#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Author: DuskPiper

from os.path import dirname, abspath
from enum import Enum

DEFAULT_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "",
    "Connection": "keep-alive",
}

PID_PAGE_TEMPLATE = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id={}"
PID_AJAX_TEMPLATE = "https://www.pixiv.net/touch/ajax/illust/details?illust_id={}"
UID_AJAX_TEMPLATE = "https://www.pixiv.net/ajax/user/{}/profile/all"
PIXIV_SHORT_LINK_TEMPLATE = "pixiv.net/i/{}"

ROOT_DIR = dirname(abspath(__file__))
DB_FOLDER_NAME = "db"
TOKEN_FILE_NAME = "token"


class ExitCode(Enum):
    TOKEN_FILE_NOT_FOUND = 0x1100


class BotMsg:
    WELCOME = "Welcome to Piper-Pixiv Bot, " \
              "I am here to help you look for artworks from pixiv.net easily" \
              "To see all supported commands, use /help "
    HELP = "Below are commands I can understand\n" \
           "/help        show this message again\n" \
           "/pid [PID]   send you artworks of given PixivID\n" \
           "/uid [UID]   send you all PixivIDs of given pixiv account\n\n\n" \
           "More functions to be delivered soon, enjoy!"
    WARN_EMPTY_PID = "Please send me a PixivID number after \"/pid\" "
    WARN_MULTI_PID = "Multiple PIDs currently supported"
    ERR_PID_NOT_FOUND = "PixivID query failure, please check PID validity"
