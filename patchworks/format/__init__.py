class PatchFile:

    def __init__(self, file):
        self._file = file
        self.records = []
        self.metadata = {}

    @classmethod
    def from_filename(cls, filename):
        return cls(open(filename, 'rb'))

    def is_patch(self):
        return NotImplemented

    def parse_metadata(self):
        return NotImplemented

    def read(self, size):
        return self._file.read(size)
