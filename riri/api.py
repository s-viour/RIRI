"""
    riri.api

    This module implements all necessary functions for interfacing
    with the riri's various components.
"""

import logging
import click
from riri.cli import finders
from riri.exceptions import *


_workers = {}
_commands = {}

logger = logging.getLogger("RIRI")


def add_worker(name, finder, downloader):
    def f(cycles, *args, **kwargs):
        find(name, cycles, *args, **kwargs)

    command = click.Command(name=name, callback=f)
    cycles_option = click.Option(param_decls=("--cycles",), default=1)
    command.params.append(cycles_option)
    finders.add_command(command)

    if name not in _workers:
        _workers[name] = (finder, downloader)
        _commands[name] = command
    else:
        logger.error("attempted to add a worker with a name that already exists")
        raise WorkerAlreadyExistsException


def get_worker_pair(name):
    if name in _workers:
        return _workers[name]
    else:
        logger.error("no worker pair with that name")
        raise InvalidFinderException


def add_worker_option(name, *args, **kwargs):
    option = click.Option(param_decls=args, **kwargs)

    command = _commands[name]
    command.params.append(option)


def add_worker_help(name, help_string):
    command = _commands[name]
    command.help = help_string


def list_finders():
    finders = []
    for name in _workers:
        finders.append(name)
    return finders


def finder_exists(name):
    try:
        get_worker_pair(name)
    except InvalidFinderException:
        return False


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
