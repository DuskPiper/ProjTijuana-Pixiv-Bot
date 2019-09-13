#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Author: DuskPiper

from Constants import *
import threading
from concurrent.futures import ThreadPoolExecutor
from re import findall

import requests


class PixivSearchCrawler:
    """
    Multi-threaded search page crawler
    """

    def __init__(self, keyword, cookies, num_results=SEARCH_MODE_LIMIT):
        self.keyword = keyword
        self.cookies = cookies
        self.num_results = num_results
        self.header = DEFAULT_HEADER
        self.pids = {}  # {PixivID : #Bookmarks}
        self.lock = threading.Lock()

    def _crawl_single_page(self, url):
        req = requests.get(url, headers=DEFAULT_HEADER, cookies=self.cookies).text
        raw_injected_data = findall(r"\"\[{(.+?)}\]\"", req)
        injected_data = raw_injected_data[0].replace("&quot;", "").split(",")
        pid, bookmarks = None, None
        for phrase in injected_data:
            if "illustId" in phrase:
                pid = phrase.split(":")[1]
            elif "bookmarkCount" in phrase:
                if not pid:
                    continue  # Honestly, this shouldn't happen
                bookmarks = int(phrase.split(":")[1])
                with self.lock:
                    self.pids[pid] = bookmarks

    def crawl(self):
        urls = [PIXIV_SEARCH_PAGE_TEMPLATE.format(self.keyword, page + 1) for page in range(SEARCH_MODE_PAGE_LIMIT)]
        with ThreadPoolExecutor(PIXIV_SEARCH_CRAWLER_THREADS_LIMIT) as executor:
            executor.map(self._crawl_single_page, urls)
        return sorted(self.pids, key=lambda entry: entry[1])[:self.num_results]
