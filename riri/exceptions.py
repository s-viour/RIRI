class RIRIException(Exception):
    """An unknown error occurred in RIRI"""


class InvalidFinderException(RIRIException):
    """There is no finder loaded with that name"""
