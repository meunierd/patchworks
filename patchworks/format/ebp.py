import json

from .ips import IPS


class EBP(IPS):

    EXTENSION = 'ebp'

    def parse_metadata(self):
        self.metadata = json.load(self._file)
