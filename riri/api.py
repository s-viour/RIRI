import logging
from riri.exceptions import InvalidFinderException

# dictionary to store class references of the finders
_workers = {}


# protected methods for adding and retrieving finders
def _add_worker(name, finder, downloader):
    _workers[name] = (finder, downloader)


def _get_worker(name):
    return _workers[name]


logger = logging.getLogger(__name__)


def get_finder(name, *args, **kwargs):
    if name in _workers:
        worker_pair = _get_worker(name)
        downloader = worker_pair[1]()
        finder = worker_pair[0](downloader, *args, **kwargs)
        downloader.start()
        return finder
    else:
        raise InvalidFinderException


def find(finder_name, cycles, *args, **kwargs):
    finder = get_finder(finder_name, *args, **kwargs)
    finder.go(cycles)