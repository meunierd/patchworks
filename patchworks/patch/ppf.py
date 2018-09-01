"""
PlayStation Patch File

"""

from .base import Parser


class PPFParser(Parser):

    EXTENSION = 'ppf'
    MAGIC = b'PPF30'
