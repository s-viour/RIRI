"""
    riri.scraper

    This is a class module that holds a framework for finders
    using selenium to scrape images.
"""


from selenium import webdriver
import riri


class Scraper(riri.Finder):
    def __init__(self, downloader, headless=False):
        super().__init__(downloader)

        options = webdriver.ChromeOptions()

        if headless:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=options)

    def scroll_down(self):
        scroll_down_script = """
                        window.scrollTo(0, document.body.scrollHeight);
                        var lenOfPage=document.body.scrollHeight;
                        return lenOfPage;
                        """
        self.driver.execute_script(scroll_down_script)
