from unittest import TestCase
import os
import riri
from riri.api import _workers


class TestFinder(riri.Finder):
    def find(self):
        return True


class TestDownloader(riri.Downloader):
    def naming_function(self, url, source):
        pass


class TestAPI(TestCase):
    def setUp(self):
        riri.add_worker("test", TestFinder, TestDownloader)

    # i really really doubt we need to test these two things but whatever
    def test_add_worker(self):
        self.assertEqual(_workers["test"], (TestFinder, TestDownloader))

    def test_get_worker_pair(self):
        worker_pair = riri.get_worker_pair("test")
        self.assertEqual(worker_pair[0], TestFinder)
        self.assertTrue(worker_pair[1], TestDownloader)

    def test_list_finders(self):
        finder_list = riri.list_finders()
        self.assertEqual(finder_list[0], "test")

    def test_get_finder(self):
        finder = riri.get_finder("test")
        self.assertTrue(isinstance(finder, TestFinder))
        self.assertTrue(isinstance(finder.downloader, TestDownloader))

    def test_find(self):
        finder = riri.get_finder("test")
        self.assertTrue(finder.find())

    def tearDown(self):
        _workers.clear()

        try:
            os.rmdir("./ralsei")
        except OSError:
            pass
