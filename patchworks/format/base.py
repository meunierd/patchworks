from patchworks import util


class Parser:

    def __init__(self, file):
        self._file = file
        self.metadata = {}

    @classmethod
    def from_filename(cls, filename):
        return cls(open(filename, 'rb'))

    def is_patch(self):
        magic = self.read(len(self.MAGIC))
        return magic == self.MAGIC

    def parse_metadata(self):
        return NotImplemented

    def read(self, size):
        return self._file.read(size)


class Record(object):

    def apply(self):
        return NotImplemented


class Applicator(object):

    def __init__(self, patch_fp, source_fp, modified_fp):
        self.patch_fp = patch_fp
        self.load_patch()
        self.source_fp = source_fp
        self.validate_source()
        self.modified_fp = modified_fp

    def apply(self):
        return NotImplemented

    def load_patch(self):
        return NotImplemented

    def validate_source(self):
        return True

    def validate_modified(self):
        return NotImplemented


class AdjustsFilesize(object):

    def expand_or_truncate(self):
        if self.patch.source_size > self.patch.modified_size:
            self.modified_fp.truncate(self.patch.modified_size)
        elif self.patch.source_size < self.patch.modified_size:
            util.expand_file(self.modified_fp, self.patch.modified_size)
