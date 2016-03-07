from . import PatchFile
from .. import util


class IPS(PatchFile):

    EXTENSION = 'ips'
    OFFSET_SIZE = 3
    DATA_SIZE = 2

    def __init__(self, file):
        self._file = file

    def is_patch(self):
        header = self._file.read(3)
        return header == b'PATCH'

    def parse_int(self, size):
        return util.int_from_bytes(self._file.read(size), 'big')

    def parse_record(self):
        offset = self.parse_int(self.OFFSET_SIZE)
        if offset == b'EOF':
            # TODO
            pass
        data_size = self.parse_int(self.DATA_SIZE)
        if not data_size:
            rle_size = self.parse_int(self.DATA_SIZE)
            data = self._file.read(1) * rle_size
        else:
            data = self._file.read(data_size)
        return offset, data

    def cut(self):
        """LunarIPS truncation extension"""
        pass
