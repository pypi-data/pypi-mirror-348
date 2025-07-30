from pathlib import Path

from xctools_kamaalio.project_updater import ProjectUpdater


def test_bump_version():
    input_project = Path(__file__).parent / "__samples__/project_files/input.pbxproj"

    result = ProjectUpdater.edit_configuration(
        project_configuration=input_project.read_text(),
        object_to_update={
            "CURRENT_PROJECT_VERSION": "22",
            "MARKETING_VERSION": "1.2.3",
        },
    )

    expected_project_result = (
        Path(__file__).parent
        / "__samples__/project_files/expected_bump_version.pbxproj"
    )
    assert result == expected_project_result.read_text()
