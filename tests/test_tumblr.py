from unittest import TestCase
import glob
import os
from riri.workers.tumblr import TumblrDownloader
from riri.workers.tumblr import Tumblr


class TestTumblr(TestCase):
    def setUp(self):
        self.downloader = TumblrDownloader(".")
        self.finder = Tumblr(self.downloader)

        self.downloader.start()

    def test_downloader_naming(self):
        url = "https://66.media.tumblr.com/26e04ce430a2a2919bcb7cd0ba8d1b29/tumblr_pllbudD8091s8am4ao1_500.png"
        filename = self.downloader.naming_function(url, "")

        self.assertEqual(filename, "tumblr_pllbudD8091s8am4ao1_500.png")

    def test_finder_find(self):
        self.finder.find()

        files = glob.glob("*.jpg")
        files.extend(glob.glob("*.png"))
        files.extend(glob.glob("*.gif"))

        self.assertNotEqual(len(files), 0)

    def tearDown(self):
        files = glob.glob("*.jpg")
        files.extend(glob.glob("*.png"))
        files.extend(glob.glob("*.gif"))

        for file in files:
            try:
                os.remove(file)
            except OSError:
                continue
