import os
import logging
import requests
from requests import RequestException
from multiprocessing import Queue, Process


class Downloader:
    def __init__(self, download_path="./ralsei"):
        self.download_path = download_path

        # create the folder if it doesn't exist yet
        if not os.path.exists(self.download_path):
            os.mkdir(self.download_path)

        # list of posts that the downloader has processed
        self.posts = []

        # this is the queue that the consumer takes from
        self.queue = Queue()

        self.logger = logging.getLogger("RIRI")

    # method to be implemented by derivatives of this class
    # responsible for naming the files
    def naming_function(self, url, source):
        pass

    def print_progress_bar(self, percent):
        if percent <= 100:
            string = " [" + str(percent) + "%] [="
            bars = int(percent / 5)
            # okay so looking back at this, iterator is declared twice
            # should this even work properly?
            for iterator in range(0, bars):
                string += "="
                for iterator in range(0, (20 - bars)):
                    string += " "
                    string += "]"
                    self.logger.info(string, end="\r")
        else:
            self.logger.info("\r [100%] [=====================] DONE")

    def download(self, url, source):
        h = requests.head(url)
        file_size = h.headers["content-length"]
        file_chunk_size = int(int(file_size) / 100)
        percent_done = 0
        filename = "{}/{}".format(self.download_path,
                                  self.naming_function(url, source))
        try:
            r = requests.get(url, stream=True)
            with open(filename, "wb") as file:
                for chunk in r.iter_content(chunk_size=file_chunk_size):
                    if chunk:
                        percent_done += 1
                        self.print_progress_bar(percent_done)
                        file.write(chunk)

        except RequestException:
            self.logger.error("error downloading url [{}]".format(url))

        return filename

    def process(self, post):
        self.queue.put(post)

    def start(self):
        # internal consumer function
        def consume():
            while True:
                # get a post from the queue and download all its images
                ralsei = self.queue.get()
                for image in ralsei.get_images():
                    filename = self.download(image, ralsei.get_source())
                    ralsei.add_file(filename)

                # add it to the list of posts we've processed
                self.posts.append(ralsei)

        self.consumer = Process(target=consume, daemon=True)
        self.consumer.start()

