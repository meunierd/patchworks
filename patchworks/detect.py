import venusian

from pathlib import Path

from patchworks import format
from patchworks.format.base import Applicator


class FormatDetector:

    def __init__(self):
        scanner = venusian.Scanner()
        scanner.scan(format)

        self.applicators = self._get_descendants(Applicator)
        self.MAX_MAGIC_LEN = max(len(a.Parser.MAGIC) for a in self.applicators)

    def detect(self, patch_path):
        with open(patch_path, 'rb') as patch_fp:
            applicator = (self.detect_by_extension(patch_fp) or
                          self.detect_by_magic(patch_fp))
        return applicator.from_filename(patch_path)

    def detect_by_magic(self, fp):
        magic = fp.read(self.MAX_MAGIC_LEN)
        for applicator in self.applicators:
            if magic.startswith(applicator.Parser.MAGIC):
                return applicator

    def detect_by_extension(self, patch_fp):
        extension = Path(patch_fp.name).suffix
        if extension:
            for applicator in self.applicators:
                if extension.endswith(applicator.Parser.EXTENSION):
                    return applicator

    def _get_descendants(self, class_):
        descendants = set(class_.__subclasses__())
        for descendant in descendants:
            descendants = descendants.union(self._get_descendants(descendant))
        return descendants
