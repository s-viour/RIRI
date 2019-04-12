class Post:
    def __init__(self, images, source):
        # initialize the images and the given source
        self.images = images
        self.source = source

        # initialize the files list
        # the downloader will set this variable
        self.files = []

    def add_file(self, path):
        self.files.append(path)

    def set_files(self, files):
        self.files = files

    def get_images(self, amount=None):
        if amount:
            return self.images[0:amount]

        return self.images

    def get_source(self):
        return self.source
