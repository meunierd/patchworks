import venusian

from patchworks import format
from patchworks.format.base import Parser

scanner = venusian.Scanner()
scanner.scan(format)


def get_descendants(class_):
    descendants = set(class_.__subclasses__())
    for descendant in descendants:
        descendants = descendants.union(get_descendants(descendant))
    return descendants


parsers = get_descendants(Parser)
