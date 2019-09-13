#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Author: DuskPiper

from Constants import *
from PixivArtworks import PixivArtworks

from urllib import request
from re import findall
import requests


def http_obj(url, headers):
    return request.urlopen(request.Request(url, headers=headers, method="GET"))


def http(url, headers):
    return request.urlopen(request.Request(url, headers=headers, method="GET")).read().decode("utf-8", "ignore")


class PixivHelper:

    @staticmethod
    def get_all_pid_by_uid(uid):
        """
        Web-query all artworks' PIDs of a given composer (given by composer's UserID)
        :param uid: UserID for pixiv, a string of number
        :return: list of PIDs
        """
        url = UID_AJAX_TEMPLATE.format(str(uid))
        page = http_obj(url, DEFAULT_HEADER)
        if page.code != 200:
            raise Exception("Pixiv Page Error:", page.code)
        all_raw_pid = findall('"[0-9]+":null', page.read().decode("utf-8", "ignore"))
        return [raw_pid.split(':')[0].strip('"') for raw_pid in all_raw_pid]

    @staticmethod
    def download_artworks_by_pid(pid):
        """
        Web download images with a given PID
        :param pid: Pixiv ID, a string of number
        :return: PixivArtworks object
        """
        header = DEFAULT_HEADER.copy()
        header["Referer"] = PID_PAGE_TEMPLATE.format(pid)
        url = PID_AJAX_TEMPLATE.format(pid)
        result = http(url, header)
        all_raw_image_url = set(findall('"url_big":"[^"]*"', result))
        all_image_url = [str(iurl.replace('\\', '').split(':', 1)[-1]).strip('"') for iurl in all_raw_image_url]
        uid = str(findall('"user_id":"[^"]*"', result)[0].split(':', 1)[-1].strip('"'))
        artworks = PixivArtworks(pid, uid)
        for image_url in all_image_url:
            image = http_obj(image_url, header)
            if image.code != 200:
                # raise Exception("Pixiv Image: [{} | {}]".format(image.code, image_url))
                return None
            else:
                artworks.add_artwork(image_url.rsplit('/', 1)[-1], image.read())
        return artworks

    @staticmethod
    def search(keyword, cookies, num_results=SEARCH_MODE_LIMIT):
        """
        Search for key-word and return highest starred results
        :param keyword: searched key-word
        :param cookies: cookies for log-in
        :param num_results: number of results
        :return: [PixivIDs]
        """
        urls = [PIXIV_SEARCH_PAGE_TEMPLATE.format(keyword, page + 1) for page in range(SEARCH_MODE_PAGE_LIMIT)]
        pids = {}  # {PixivID : #bookmark}
        for url in urls:
            req = requests.get(url, headers=DEFAULT_HEADER, cookies=cookies).text
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
                    pids[pid] = bookmarks
        return sorted(pids, key=lambda entry: entry[1])[:num_results]


if __name__ == "__main__":
    test_uid = "11246082"
    test_pid = "74542813"
    test_search_word = "レミリア"

    from os.path import join
    with open(join(ROOT_DIR, COOKIES_FILE_NAME), "r") as f:
        cook = {}
        for row in f.read().split(";"):
            k, v = row.strip().split("=", 1)
            cook[k] = v
    print(PixivHelper.search(test_search_word, cook))
