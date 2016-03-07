from datetime import datetime

from . import PatchFile
from .. import util


class Ninja2(PatchFile):

    EXTENSION = 'rup'
    DATA_TYPE = {
        b'\x00': 'raw',
        b'\x01': 'NES',
        b'\x02': 'FDS',
        b'\x03': 'SFC',
        b'\x04': 'GB',
        b'\x05': 'SMS',
        b'\x07': 'MD',
        b'\x08': 'PCE',
        b'\x09': 'LYNX',
    }

    def __init__(self, file):
        self._file = file
        self.records = []
        self.metadata = {}

    def is_patch(self):
        self._file.seek(0)
        header = self.read(6)
        return header == b'NINJA2'

    def parse_metadata(self):
        field_spec = [
            ("encoding", 1),
            ("author", 84),
            ("version", 11),
            ("title", 256),
            ("genre", 48),
            ("language", 48),
            ("date", 8),
            ("website", 512),
            ("description", 1074),
        ]

        for field, size in field_spec:
            field_data = self.read(size)
            self.metadata[field] = util.zero_padded_bytes_to_string(field_data)

        self.format_description()
        self.format_date()

    def parse_eof(self):
        self._file.close()

    def parse_records(self):
        command = self.read(1)
        while command != b'\x00':
            if command == b'\x01':
                self.parse_file()
            elif command == b'\x02':
                self.parse_record()
            else:
                raise Exception('Unknown command')
        self.parse_eof()

    def parse_record(self):
        offset = self.parse_int()
        data_size = self.parse_int()
        data = self.read(data_size)
        self.records.append((offset, data))

    def parse_file_metadata(self):
        self.parse_filename()  # TODO: multi-file patch support
        self.metadata['type'] = self.DATA_TYPE[self.read(1)]
        self.metadata['source'] = {}
        self.metadata['modified'] = {}
        self.metadata['source']['size'] = self.parse_int()
        self.metadata['modified']['size'] = self.parse_int()
        self.metadata['source']['md5'] = self.read(16)
        self.metadata['modified']['md5'] = self.read(16)

    def parse_filename(self):
        filename_size = self.parse_int()
        return self.read(filename_size) if filename_size else None

    def parse_int(self):
        return util.int_from_bytes(self.read(ord(self.read(1))))

    def format_description(self):
        info = self.metadata['description']
        self.metadata['description'] = info.replace('\\n', '\n')

    def format_date(self):
        date = self.metadata['date']
        if date:
            self.metadata['date'] = datetime.strptime(date, "%Y%m%d").date()
