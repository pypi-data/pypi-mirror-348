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
@click.option("--project")
@click.option("--workspace")
def build(configuration, scheme, destination, project, workspace):
    XcTools.build(
        configuration=configuration,
        scheme=scheme,
        destination=destination,
        project=project,
        workspace=workspace,
    )
