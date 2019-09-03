#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Author: DuskPiper

from Constants import *
from os.path import *
from os import makedirs, umask, listdir, remove, removedirs
import logging


class DBHelper:

    def __init__(self):
        self.db_path = ROOT_DIR + "/" + DB_FOLDER_NAME + "/"
        self.pid_to_uid = {}  # {pid: uid} ToDo: use SQLite instead
        self.size_in_bytes = 0  # data folder size
        self.size = 0  # artworks quantity
        self.history = []  # for LRU check
        self.scan_db_folder()

    def print_db_status(self):
        print("============Database Summary=============")
        print("UID quantity:      ", len(listdir(self.db_path)))
        print("Artworks quantity: ", self.size)
        print("Database size:      {:.4f} MB".format(self.size_in_bytes / 1024 / 1024))
        print("=========================================")

    def add(self, uid, image_name, image):
        """
        Save an image into db folder
        :param uid: Artwork composer UID, a string of number
        :param image_name: image file name, formatted as {pid}_p{No.}.{file-format}
        :param image: image content stream
        :return: True if succeed, False if not
        """
        pid = image_name.split("_")[0]
        self._update_history(pid)
        if pid in self.pid_to_uid:  # artwork already present
            return True
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
            logging.error("Failure saving image: " + image_name)
            return False
        else:
            self.pid_to_uid[pid] = uid
            self.size += 1
            self.size_in_bytes += getsize(file_path)
            logging.info("Saved image: " + image_name)
            return True

    def delete(self, pid):
        """
        Delete all artworks of given PID
        :param pid: Pixiv-ID, a string of number
        :return: None
        """
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
                    logging.error("Failed to remove image: " + file_name)
                else:
                    self.size_in_bytes -= file_size
                    self.size -= 1
                    logging.info("Deleted file: " + file_name)
        self.pid_to_uid.pop(pid)
        self.history.remove(pid)
        if not listdir(uid_path):  # UID folder empty
            try:
                old_mask = umask(000)  # to get permission on some OS
                removedirs(uid_path)
                umask(old_mask)  # return permission
            except IOError:
                logging.error("Failed to delete empty UID folder " + uid)
            else:
                logging.info("Deleted empty UID folder" + uid)

    def search(self, pid):
        """
        Search for PID
        :param pid: Pixiv-ID, a string of number
        :return: list of dirs of files of given pid
        """
        if pid not in self.pid_to_uid:
            return []
        self._update_history(pid)
        uid = self.pid_to_uid[pid]
        uid_path = join(self.db_path, uid)
        all_files_under_path = listdir(uid_path)
        return [join(uid_path, file_name) for file_name in all_files_under_path if pid in file_name]

    def scan_db_folder(self):
        """Re-scan db-folder and re-construct db"""
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
        self._validate_history()
        logging.info("Updated DB")
        self.print_db_status()

    def _update_history(self, pid):
        """Update Recent-Used pid, in case of LRU deletion"""
        if pid in self.history:
            self.history.remove(pid)
        self.history.append(pid)

    def _validate_history(self):
        """De-duplicate and remove bad pid"""
        history_len = len(self.history)
        duplicate_checker = set([])
        for i in range(history_len - 1, -1, -1):
            pid = self.history[i]
            if pid in duplicate_checker:
                self.history.pop(i)
            else:
                duplicate_checker.add(pid)
        for pid in self.history:
            if pid not in self.pid_to_uid:
                self.history.remove(pid)


# db_helper = DBHelper  # Singleton
