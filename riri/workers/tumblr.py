"""
    riri.tumblr

    This is a Finder module responsible for scraping images from Tumblr
    using selenium. It does NOT use the Tumblr API.
"""

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import riri


class Tumblr(riri.Scraper):
    def __init__(self, downloader, headless=False, url=None):
        super().__init__(downloader=downloader, headless=headless)

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

                ralsei = riri.Post(images, source)
                self.process_post(ralsei)

            # if we get this error, it's because there's no images in the post
            except NoSuchElementException:
                # just continue
                continue

            except StaleElementReferenceException:
                self.logger.error("error extracting images from post {}".format(source))
                continue

        self.scroll_down()


class TumblrDownloader(riri.Downloader):
    def naming_function(self, url, source):
        return url[url.find("tumblr_"):]


riri.add_worker("tumblr", Tumblr, TumblrDownloader)
riri.add_worker_option("tumblr", "--headless", is_flag=True)
riri.add_worker_option("tumblr", "--url")
riri.add_worker_help("tumblr", """retrieves images from Tumblr without an API key via browser""")