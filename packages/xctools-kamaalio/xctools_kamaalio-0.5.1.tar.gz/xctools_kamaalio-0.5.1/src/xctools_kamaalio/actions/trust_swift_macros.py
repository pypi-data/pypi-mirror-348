import click

from xctools_kamaalio.xctools import XcTools


@click.command(context_settings={"ignore_unknown_options": True})
@click.option("--trust-file", required=True)
def trust_swift_macros(trust_file):
    XcTools.trust_swift_macros(trust_file_path=trust_file)
