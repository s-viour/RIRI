"""
    riri.finder

    Class module that holds the Finder class
"""

import logging


class Finder:
    def __init__(self, downloader):
        self.logger = logging.getLogger("RIRI")
        self.downloader = downloader

    # method to be implemented by derivatives of this class
    def find(self):
        pass

    def process_post(self, post):
        self.downloader.process(post)

    def go(self, num_times):
        for i in range(0, num_times):
            self.find()
