#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Author: DuskPiper

from PixivSearchCrawler import PixivSearchCrawler

from Constants import *
from random import sample
from time import time


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner


@singleton
class Remilia:  # Singleton, initialized upon use

    def __init__(self):
        self.pids = set([])
        self.keyword = "レミリア 東方Project1000users入り"
        self.update_period = 24 * 60 * 60  # one day
        self.latest_update = time()  # for periodically check updates
        self._crawl_from_web()

    def get(self):
        self._notify_update_checker()
        if not self.pids:
            return None
        return sample(self.pids, 1)[0]

    def _notify_update_checker(self):
        if time() - self.latest_update > self.update_period:
            self._crawl_from_web()
            self.latest_update = time()

    def _crawl_from_web(self):
        crawler = PixivSearchCrawler(self.keyword, num_results=999, pages=16)
        self.pids = crawler.crawl(safemode=True)
        del crawler

    ''' Considering the amount to be crawled is not significant, we don't need this for remilia theme
    
    from os.path import exists, join
    def _read_from_local(self):
        file_path = join(ROOT_DIR, REMILIA_FILE_NAME)
        if not exists(file_path):
            return False

        def is_valid_pid(pid):
            if not pid:
                return False
            try:
                int(pid)
            except ValueError:
                return False
            return True

        with open(file_path, "r") as sakuya:
            raw_pids = sakuya.readlines()
            self.pids.update([pid for pid in raw_pids if is_valid_pid(pid)])
        return True

    def _save_to_local(self):
        file_path = join(ROOT_DIR, REMILIA_FILE_NAME)
        with open(file_path, "w") as sakuya:
            sakuya.writelines(self.pids)
    '''


if __name__ == "__main__":
    from os.path import join
    with open(join(ROOT_DIR, COOKIES_FILE_NAME), "r") as f:
        cook = {}
        for row in f.read().split(";"):
            k, v = row.strip().split("=", 1)
            cook[k] = v
    COOKIES = cook
    for i in range(5):
        print(Remilia().get())
