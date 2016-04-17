from . import PatchFile
from .. import util


class IPS(PatchFile):

    EXTENSION = 'ips'

    def __init__(self, file, romexpander=None):
        super().__init__(file)
        self.romexpander = romexpander

    def is_patch(self):
        header = self.read(5)
        return header == b'PATCH'

    def parse_int(self, size):
        return util.int_from_bytes(self.read(size), 'big')

    def parse_records(self):
        OFFSET_SIZE = 3
        DATA_SIZE = 2

        for offset in iter(lambda: self.read(OFFSET_SIZE), b'EOF'):
            data_size = self.parse_int(DATA_SIZE)
            if not data_size:
                rle_size = self.parse_int(DATA_SIZE)
                data = self.read(1) * rle_size
            else:
                data = self.read(data_size)
            yield (offset, data)

    def cut(self):
        """LunarIPS truncation extension"""
        pass
