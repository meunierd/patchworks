from patchworks import util


class Patch(object):

    def __init__(self, fp):
        self.fp = fp
        self.metadata = {}

    def apply(self):
        return NotImplemented

    def read(self, size):
        return self.fp.read(size)

    @classmethod
    def from_filename(cls, filename):
        return cls(open(filename, 'rb'))

    def is_patch(self):
        magic = self.fp.read(len(self.MAGIC))
        return magic == self.MAGIC


class AdjustsFilesize:

    def expand_or_truncate(self):
        if self.patch.source_size > self.patch.modified_size:
            self.modified_fp.truncate(self.patch.modified_size)
        elif self.patch.source_size < self.patch.modified_size:
            util.expand_file(self.modified_fp, self.patch.modified_size)


class CopiesSource:

    def copy_source_to_modified(self, source_fp, target_fp):
        buffer_size = 1024
        source_fp.seek(0)
        for data in iter(lambda: source_fp.read(buffer_size), b''):
            target_fp.write(data)

# Main object should be a Patch class with an apply method that acts on source
# and target file pointers.
