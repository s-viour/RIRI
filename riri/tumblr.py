from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from riri.finder import Finder
from riri.downloader import Downloader
from riri.post import Post
from riri import api


class TumblrFinder(Finder):
    def __init__(self, downloader, url=None, headless=False):
        super().__init__(downloader)

        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=options)

        if not url:
            self.url = "https://www.tumblr.com/search/ralsei"
        else:
            self.url = url
        self.driver.get(self.url)

    def find(self):
        posts = self.driver.find_elements_by_tag_name("article")
        self.logger.info("# of posts found: {}".format(len(posts)))
        for post in posts:
            try:
                source = post.find_element_by_class_name("post_header")
                source = source.find_element_by_tag_name("a").get_attribute("href")
                images = post.find_element_by_class_name("post_body")
                images = images.find_elements_by_tag_name("img")

                for i in range(0, len(images)):
                    images[i] = images[i].get_attribute("src")

                ralsei = Post(images, source)
                self.process_post(ralsei)

            # if we get this error, it's because there's no images in the post
            except NoSuchElementException:
                # just continue
                continue

            except StaleElementReferenceException:
                self.logger.error("error extracting images from post {}".format(source))
                continue

        scroll_down_script = """
                window.scrollTo(0, document.body.scrollHeight);
                var lenOfPage=document.body.scrollHeight;
                return lenOfPage;
                """
        self.driver.execute_script(scroll_down_script)


class TumblrDownloader(Downloader):
    def naming_function(self, url, source):
        return url[url.find("tumblr_"):]


api.add_worker("tumblr", TumblrFinder, TumblrDownloader)