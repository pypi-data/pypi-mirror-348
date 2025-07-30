import click

from xctools_kamaalio.xctools import XcTools


@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "--target",
    type=click.Choice(["ios", "macos"], case_sensitive=False),
    required=True,
)
@click.option("--file", required=True)
@click.option("--username", required=True)
@click.option("--password", required=True)
def upload(target, file, username, password):
    XcTools.upload(target=target, file=file, username=username, password=password)
