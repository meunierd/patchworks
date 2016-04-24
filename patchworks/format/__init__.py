class PatchFile:

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

    def apply(self, source_file, modified_file):
        pass
