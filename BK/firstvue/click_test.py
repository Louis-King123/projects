import click


@click.command()
@click.option('--hi', prompt=True)
@click.option('--name', prompt=True)
def hello(hi, name):
    click.echo('%s %s!' % (hi, name))


if __name__ == '__main__':
    hello()
