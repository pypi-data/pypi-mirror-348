import click

from xctools_kamaalio.xctools import XcTools


@click.command(context_settings={"ignore_unknown_options": True})
@click.option("--build-number", type=click.INT)
@click.option("--version-number")
def bump_version(build_number, version_number):
    XcTools.bump_version(build_number=build_number, version_number=version_number)
