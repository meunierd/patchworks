class PatchFile:
    def is_patch(self):
        return NotImplemented

    def parse_metadata(self):
        return NotImplemented

    def read(self, size):
        return self._file.read(size)


class SourceFile:

    def __init__(self):
        self.metadata = {}


class ModifiedFile:

    def __init__(self):
        self.metadata = {}
