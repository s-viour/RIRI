"""
    riri.cli

    All the logic regarding the CLI, except for the
    finders bootstrapping themselves into a command.
"""


import click
import riri


@click.group()
def main():
    pass


@main.command("list")
def cmd_list():
    """list all workers available"""
    finders = riri.list_finders()
    click.echo("Currently available finders: ")
    click.echo("".join("\t" + str(f) for f in finders))


@main.group("find")
def finders():
    """find images with the given finder"""
    pass
