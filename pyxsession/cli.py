import click
from pyxsession.config import load_config


@click.command()
def main():
    # TODO: Anything lmao

    # TODO: Pass any cli parameters in that might override the config
    print(load_config())
