import argparse

parser = argparse.ArgumentParser('patchworks', description='ROM patching swiss-army knife.')
subparsers = parser.add_subparsers()

apply_parser = subparsers.add_parser('apply')
apply_parser.add_argument('PATCH')
apply_parser.add_argument('SOURCE')
apply_parser.add_argument('TARGET')

create_parser = subparsers.add_parser('create')
create_parser.add_argument('-f', '--format', required=True)
create_parser.add_argument('SOURCE')
create_parser.add_argument('MODIFIED')
create_parser.add_argument('PATCH')

info_parser = subparsers.add_parser('info')
info_parser.add_argument('PATCH')


if __name__ == '__main__':
    print(vars(parser.parse_args()))
