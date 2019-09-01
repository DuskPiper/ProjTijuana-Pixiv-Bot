#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Author: DuskPiper

from os.path import dirname
from os.path import abspath

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

ROOT_DIR = dirname(abspath(__file__))
DB_FOLDER_NAME = "db"
