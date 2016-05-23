import click


@click.group(name='patchworks')
def cli():
    pass


@cli.command()
@click.argument('patch', type=click.Path(exists=True))
@click.argument('source', type=click.Path(exists=True))
@click.argument('modified', type=click.Path(exists=False))
def apply(patch, source, modified):
    # detect patch
    # apply patch
    pass


@cli.command()
@click.option('--format')
def create():
    pass


if __name__ == '__main__':
    cli()
