import binascii

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

    def is_patch(self):
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

        for field, field_size in field_spec:
            field_data = self.read(field_size)
            self.metadata[field] = util.zero_padded_bytes_to_string(field_data)

        self.format_description()
        self.format_date()

    def parse_records(self):
        PARSE_FILE = b'\x01'
        PARSE_RECORD = b'\x02'

        for command in iter(lambda: self.read(1), b'\x00'):
            if command == PARSE_FILE:
                self.parse_file()
            elif command == PARSE_RECORD:
                self.parse_record()

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
        self.metadata['source']['md5'] = self.parse_md5()
        self.metadata['modified']['md5'] = self.parse_md5()

    def parse_md5(self):
        return binascii.hexlify(self.read(16)).decode()

    def parse_filename(self):
        filename_size = self.parse_int()
        return self.read(filename_size) if filename_size else None

    def parse_int(self):
        return util.int_from_bytes(self.read(util.int_from_bytes(self.read(1))))

    def format_description(self):
        self.metadata['description'] = self.metadata['description'].replace('\\n', '\n')

    def format_date(self):
        date = self.metadata['date']
        if date:
            self.metadata['date'] = datetime.strptime(date, "%Y%m%d").date()
