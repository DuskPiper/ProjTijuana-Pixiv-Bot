#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Author: DuskPiper


class PixivArtworks:

    def __init__(self, pid, uid):
        self.pid = str(pid)
        self.uid = str(uid)
        self.artworks = {}  # {image_name:image}

    def add_artwork(self, image_name, image):
        self.artworks[image_name] = image
