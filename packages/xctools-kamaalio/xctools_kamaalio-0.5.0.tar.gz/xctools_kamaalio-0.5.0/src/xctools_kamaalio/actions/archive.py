import click

from xctools_kamaalio.xctools import XcTools


@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "--configuration",
    type=click.Choice(["Debug", "Release"], case_sensitive=False),
    required=True,
)
@click.option("--scheme", required=True)
@click.option("--destination", required=True)
@click.option(
    "--sdk",
    type=click.Choice(["iphoneos", "macosx"], case_sensitive=False),
    required=True,
)
@click.option("--archive-path", required=True)
@click.option("--project")
@click.option("--workspace")
def archive(configuration, scheme, destination, sdk, archive_path, project, workspace):
    XcTools.archive(
        scheme=scheme,
        configuration=configuration,
        destination=destination,
        sdk=sdk,
        archive_path=archive_path,
        project=project,
        workspace=workspace,
    )
