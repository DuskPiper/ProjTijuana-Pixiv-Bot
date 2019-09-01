#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Author: DuskPiper

from Constants import *
from os.path import *
from os import makedirs, umask, listdir


class DBHelper:

    def __init__(self):
        self.db_path = ROOT_DIR + "/" + DB_FOLDER_NAME + "/"
        self.db = {}  # {uid:set(pid)} ToDo: use SQLite instead
        self.pid_to_uid = {}  # {pid: uid} ToDo: use SQLite instead
        self.size_in_bytes = 0  # data folder size
        self.size = 0  # artwork quantity
        self.history = []  # for LRU check
        self._scan_db_folder()

    def print_db_status(self):
        print("============Database Summary=============")
        print("UID quantity:      ", len(self.db))
        print("Artworks quantity: ", self.size)
        print("Database size:      {:.4f} MB".format(self.size_in_bytes / 1024 / 1024))
        print("=========================================")

    def add(self, uid, image_name, image):
        pid = image_name.split("_")[0]
        if pid in self.pid_to_uid:  # artwork already present
            return
        try:
            save_path = "/".join((ROOT_DIR, DB_FOLDER_NAME, uid)) + "/"
            if not exists(save_path):
                old_mask = umask(000)  # to get permission on some OS
                makedirs(save_path, 0o0755)
                umask(old_mask)  # return permission
            file_path = join(save_path, image_name)
            image_writer = open(file_path, "wb")
            image_writer.write(image)
            image_writer.close()
        except IOError:
            print(">x> Failure saving image: " + image_name)
        else:
            if uid not in self.db:
                self.db[uid] = set([])
            self.db[uid].add(pid)
            self.pid_to_uid[pid] = uid
            self.size += 1
            self.size_in_bytes += getsize(file_path)
            print(">>> Saved image: " + image_name)

    def _scan_db_folder(self):
        self.size_in_bytes = 0
        self.size = 0
        self.db = {}
        self.pid_to_uid = {}
        all_file_name = listdir(self.db_path)
        all_uid = (folder for folder in all_file_name if isdir(folder))
        for uid in all_uid:
            all_pid = set([])
            uid_dir = join(self.db_path, uid)
            all_image_name = listdir(uid_dir)
            self.size += len(all_image_name)
            for image_name in all_image_name:
                pid = image_name.split("_")[0]
                all_pid.add(pid)
                self.size_in_bytes += getsize(join(uid_dir, image_name))
                self.pid_to_uid[pid] = uid
            self.db[uid] = all_pid
        print(">>> Updated DB")
        self.print_db_status()


db_helper = DBHelper  # Singleton
