import click

from xctools_kamaalio.xctools import XcTools


@click.command(context_settings={"ignore_unknown_options": True})
@click.option("--archive-path", required=True)
@click.option("--export-options", required=True)
def export_archive(archive_path, export_options):
    XcTools.export_archive(archive_path=archive_path, export_options=export_options)
