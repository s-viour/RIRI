import logging
from riri.exceptions import *


# dictionary to store class references of the finders
_workers = {}

logger = logging.getLogger(__name__)


def add_worker(name, finder, downloader):
    if name not in _workers:
        _workers[name] = (finder, downloader)
    else:
        logger.error("attempted to add a worker with a name that already exists")
        raise WorkerAlreadyExistsException


def set_worker(name, finder, downloader):
    _workers[name] = (finder, downloader)


def get_worker_pair(name):
    if name in _workers:
        return _workers[name]
    else:
        logger.error("no worker pair with that name")
        raise InvalidFinderException


def list_finders():
    finders = []
    for name in _workers:
        finders.append(name)
    return finders


def get_finder(name, *args, **kwargs):
    if name in _workers:
        worker_pair = get_worker_pair(name)
        downloader = worker_pair[1]()
        finder = worker_pair[0](downloader, *args, **kwargs)
        downloader.start()
        return finder
    else:
        logger.error("no finder with that name")
        raise InvalidFinderException


def find(finder_name, cycles, *args, **kwargs):
    finder = get_finder(finder_name, *args, **kwargs)
    finder.go(cycles)