from unittest import TestCase
from riri import Post


class TestPost(TestCase):
    def setUp(self):
        self.urls = ["https://66.media.tumblr.com/e88a834263fdf9882da15f86d2c78bbb/tumblr_inline_pmy3lb4B5Q1tydtov_400.png",
                     "https://66.media.tumblr.com/6cff0cb2f7012d7cfd5a325d33f0afa2/tumblr_inline_pmy3lco4QU1tydtov_400.png",
                     "https://66.media.tumblr.com/ce7d4dfa4fc9502e6ba4cd641fb5c6da/tumblr_inline_pmy3lcbyRs1tydtov_400.png",
                     "https://66.media.tumblr.com/a033515c4e601840edabb241c41dfb94/tumblr_inline_pmy3lcvxaw1tydtov_400.png"]
        self.source = "https://amemethyst.tumblr.com/post/182815857983/deltarune-valentines"
        self.post = Post(self.urls, self.source)

    def test_add_file(self):
        self.post.add_file("./")
        self.assertEqual(self.post.files[0], "./")

    def test_set_files(self):
        files = ["./", "..", "."]
        self.post.set_files(files)
        self.assertEqual(self.post.files, files)

    def test_get_images(self):
        all_images = self.post.get_images()
        self.assertEqual(self.urls, all_images)

        one_image = self.post.get_images(1)
        self.assertEqual(self.urls[0:1], one_image)

    def test_get_source(self):
        source = self.post.get_source()
        self.assertEqual(source, self.source)
