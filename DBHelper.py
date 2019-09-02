#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Author: DuskPiper

from Constants import *
from os.path import *
from os import makedirs, umask, listdir, remove, removedirs


class DBHelper:

    def __init__(self):
        self.db_path = ROOT_DIR + "/" + DB_FOLDER_NAME + "/"
        self.pid_to_uid = {}  # {pid: uid} ToDo: use SQLite instead
        self.size_in_bytes = 0  # data folder size
        self.size = 0  # artworks quantity
        self.history = []  # for LRU check
        self._scan_db_folder()

    def print_db_status(self):
        print("============Database Summary=============")
        print("UID quantity:      ", len(listdir(self.db_path)))
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
            self.pid_to_uid[pid] = uid
            self.size += 1
            self.size_in_bytes += getsize(file_path)
            print(">>> Saved image: " + image_name)

    def delete(self, pid):
        if pid not in self.pid_to_uid:  # artwork not exists
            return
        uid = self.pid_to_uid[pid]
        uid_path = join(self.db_path, uid)
        all_files_under_path = listdir(uid_path)
        for file_name in all_files_under_path:
            if pid in file_name:
                file_path = join(uid_path, file_name)
                file_size = getsize(file_path)
                try:
                    remove(file_path)
                except IOError:
                    print(">x> Failed to remove image: " + file_name)
                else:
                    self.size_in_bytes -= file_size
                    self.size -= 1
                    print(">>> Deleted file: " + file_name)
        self.pid_to_uid.pop(pid)
        if not listdir(uid_path):  # UID folder empty
            try:
                old_mask = umask(000)  # to get permission on some OS
                removedirs(uid_path)
                umask(old_mask)  # return permission
            except IOError:
                print(">x> Failed to delete empty UID folder " + uid)
            else:
                print(">>> Deleted empty UID folder" + uid)

    def search(self, pid):
        if pid not in self.pid_to_uid:
            return []
        uid = self.pid_to_uid[pid]
        uid_path = join(self.db_path, uid)
        all_files_under_path = listdir(uid_path)
        return [join(uid_path, file_name) for file_name in all_files_under_path if pid in file_name]

    def _scan_db_folder(self):
        self.size_in_bytes = 0
        self.size = 0
        self.pid_to_uid.clear()
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
        print(">>> Updated DB")
        self.print_db_status()


db_helper = DBHelper  # Singleton
