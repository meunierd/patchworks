import codecs
import json

from .ips import IPS


class EBPatcher(IPS):

    EXTENSION = 'ebp'

    def parse_metadata(self):
        reader = codecs.getreader('utf-8')
        self.metadata = json.load(reader(self._file))
