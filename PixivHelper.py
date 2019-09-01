#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Author: DuskPiper

from urllib import request
from re import findall
from Constants import *
from DBHelper import db_helper


def http_obj(url, headers):
    return request.urlopen(request.Request(url, headers=headers, method="GET"))


def http(url, headers):
    return request.urlopen(request.Request(url, headers=headers, method="GET")).read().decode("utf-8", "ignore")


''' use db_helper instead
def save_image(uid, image_name, image):
    save_path = "/".join((ROOT_DIR, DB_FOLDER_NAME, uid)) + "/"
    if not exists(save_path):
        old_mask = umask(000)  # to get permission on some OS
        makedirs(save_path, 0o0755)
        umask(old_mask)  # return permission
    file_path = join(save_path, image_name)
    try:
        image_writer = open(file_path, "wb")
        image_writer.write(image)
        image_writer.close()
    except IOError:
        print(">x> Failure saving image: " + file_path)
    else:
        print(">>> Saved image: " + image_name)
'''


class PixivHelper:

    @staticmethod
    def get_all_pid_by_uid(uid):
        url = UID_AJAX_TEMPLATE.format(str(uid))
        page = http_obj(url, DEFAULT_HEADER)
        if page.code != 200:
            raise Exception("Pixiv Page Error:", page.code)
        all_raw_pid = findall('"[0-9]+":null', page.read().decode("utf-8", "ignore"))
        return [raw_pid.split(':')[0].strip('"') for raw_pid in all_raw_pid]

    @staticmethod
    def download_image_by_pid(pid):
        header = DEFAULT_HEADER.copy()
        header["Referer"] = PID_PAGE_TEMPLATE.format(pid)
        url = PID_AJAX_TEMPLATE.format(pid)
        res = http(url, header)
        all_raw_image_url = set(findall('"url_big":"[^"]*"', res))
        all_image_url = [str(iurl.replace('\\', '').split(':', 1)[-1]).strip('"') for iurl in all_raw_image_url]
        uid = str(findall('"user_id":"[^"]*"', res)[0].split(':', 1)[-1].strip('"'))
        for image_url in all_image_url:
            image = http_obj(image_url, header)
            if image.code != 200:
                raise Exception("Pixiv Image: [{} | {}]".format(image.code, image_url))
            else:
                #db_helper.add(uid, image_url.rsplit('/', 1)[-1], image.read())
                # ToDo 写一个main来调用两个helper，而不是由这个helper调用另一个


if __name__ == '__main__':
    test_uid = '11246082'
    test_pid = '74542813'
    PixivHelper.download_image_by_pid(test_pid)
