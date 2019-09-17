#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Author: DuskPiper

from os.path import dirname, abspath, join
from enum import Enum
import logging

# Config logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
LOGGER = logging.getLogger(__name__)

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
PIXIV_SEARCH_PAGE_TEMPLATE = "https://www.pixiv.net/search.php?word={}&order=date_d&p={}"
PIXIV_SEARCH_PAGE_SAFE_TEMPLATE = "https://www.pixiv.net/search.php?word={}&order=date_d&p={}&mode=safe"


ROOT_DIR = dirname(abspath(__file__))
DB_FOLDER_NAME = "db"
TOKEN_FILE_NAME = "token"
COOKIES_FILE_NAME = "cookies"
REMILIA_FILE_NAME = "remilia"

UID_MODE_LIMIT = 5  # maximum PIDs queried
SEARCH_MODE_LIMIT = 5  # maximum search results
SEARCH_MODE_PAGE_LIMIT = 28  # maximum crawler pages
SEARCH_MODE_KEYWORD_LENGTH_LIMIT = 30  # keyword string longer than this will be cropped
PIXIV_SEARCH_CRAWLER_THREADS_LIMIT = 5  # maximum threads used to crawl search page


class ExitCode(Enum):
    TOKEN_FILE_NOT_FOUND = 0x1100
    COOKIES_FILE_NOT_FOUND = 0x1101


class BotMsg:
    WELCOME = "Welcome to Piper-Pixiv Bot, " \
              "I am here to help you look for artworks from pixiv.net easily" \
              "To see all supported commands, use /help "
    HELP = "Below are commands I can understand\n" \
           "/help            show this message again\n" \
           "/pid [PID]       artworks of given PixivID\n" \
           "/uid [UID]       recent artworks of account\n" \
           "/search [words]  search for key words\n" \
           "/erosearch [w.]  careful, may contain 18x contents\n" \
           "/remilia         a random レミリア artwork\n" \
           "/downpid [PID]   original-sized artworks for download\n\n" \
           "More functions to be delivered soon, enjoy!"

    CMD_PID_WARN_EMPTY_PID = "Please send me a PixivID number after \"/pid\" "
    CMD_PID_WARN_MULTI_PID = "Multiple PIDs currently unsupported"
    CMD_PID_ERR_PID_NOT_FOUND = "PixivID query failure, please check PID validity"

    CMD_UID_WARN_EMPTY_UID = "Please send me a Pixiv UserID number after \"/uid\" "
    CMD_UID_WARN_MULTI_UID = "Multiple UIDs currently unsupported"
    CMD_UID_ERR_UID_NOT_FOUND = "Pixiv user-ID query failure, please check UID validity"
    CMD_UID_INFO_LIMIT_REACHED = "Only showing recent {} PixivID results".format(UID_MODE_LIMIT)

    CMD_DOWNPID_ERR_FAIL_TO_SEND = "One image not sent, it may be too large"

    CMD_SEARCH_EMPTY_ARGS = "Please also send me keywords after \"/search\""
    CMD_SEARCH_EMPTY_RESULTS = "No results... Try shorten your keywords?"

    CMD_REMILIA_EMPTY_RESULTS = "Something is wrong here... Can't find any レミ"


# Load pixiv.net cookies (for searching)
COOKIES = {}
try:
    cookies_loader = open(join(ROOT_DIR, COOKIES_FILE_NAME), "r")
    raw_cookies = cookies_loader.read()
    cookies_loader.close()
    for row in raw_cookies.split(";"):
        cookies_key, cookies_val = row.strip().split("=", 1)
        COOKIES[cookies_key] = cookies_val
    LOGGER.info("Loaded cookies")
except IOError:
    LOGGER.critical("Failed to read cookies")
    LOGGER.error("Cookies file should be in project-dir and named \"{}\"".format(COOKIES_FILE_NAME))
    exit(ExitCode.COOKIES_FILE_NOT_FOUND)
