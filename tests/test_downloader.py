import os
import time
from unittest import TestCase
from riri import Downloader, Post


class TestDownloader(TestCase):
    def setUp(self):
        self.urls = ["https://66.media.tumblr.com/26e04ce430a2a2919bcb7cd0ba8d1b29/tumblr_pllbudD8091s8am4ao1_500.png"]
        self.source = "http://potoobrigham.tumblr.com/post/182140716011/pacify"
        self.downloader = Downloader(".")

        def naming_func(url, source):
            return "ralsei.png"

        self.downloader.naming_function = naming_func

    def test_download(self):
        self.filename = self.downloader.download(self.urls[0], self.source)

        self.assertTrue(os.path.exists(self.filename))

    def test_process(self):
        post = Post(self.urls, self.source)

        self.downloader.process(post)
        retrieved_post = self.downloader.queue.get()

        self.assertEqual(post.get_source(), retrieved_post.get_source())

    def test_start(self):
        self.downloader.start()

        self.assertTrue(self.downloader.consumer.is_alive())

    def test_downloader(self):
        self.downloader.start()

        post = Post(self.urls, self.source)

        self.downloader.process(post)
        # sleep for a bit to allow the post to download asynchronously
        time.sleep(1)

        self.assertTrue(os.path.exists("./ralsei.png"))

    def tearDown(self):
        try:
            os.remove("./ralsei.png")
        except OSError:
            pass
