from pathlib import Path

from kamaaalpy.dicts import omit_empty


class ProjectUpdater:
    project_configurations: list[Path]

    def __init__(self) -> None:
        project_configurations: list[Path] = []
        for path in Path.cwd().glob("**/*"):
            if path.name != "project.pbxproj":
                continue

            project_configurations.append(path)

        if len(project_configurations) == 0:
            raise ProjectUpdaterException("No project path found")

        self.project_configurations = project_configurations

    def bump_version(self, build_number: int | None, version_number: str | None):
        has_changes = self.__edit(
            object_to_update=omit_empty(
                {
                    "CURRENT_PROJECT_VERSION": str(build_number),
                    "MARKETING_VERSION": version_number,
                }
            )
        )
        if has_changes:
            print("Applied changes to xcode project")
        else:
            print("No changes where needed")

    @staticmethod
    def edit_configuration(
        project_configuration: str, object_to_update: dict[str, str]
    ):
        project_configuration_file_lines = project_configuration.splitlines()
        keys_to_update = object_to_update.keys()
        has_changes = False
        for line_number, line in enumerate(project_configuration_file_lines):
            for key in keys_to_update:
                if key not in line:
                    continue

                amount_of_tabs = line.count("\t")
                tabs = "\t" * amount_of_tabs
                project_configuration_file_lines[line_number] = (
                    f"{tabs}{key} = {object_to_update[key]};"
                )
                has_changes = True
                break

        if not has_changes:
            return

        if len(project_configuration_file_lines[-1]) != 0:
            project_configuration_file_lines.append("")

        return "\n".join(project_configuration_file_lines)

    def __edit(self, object_to_update: dict[str, str]):
        if object_to_update == {}:
            return False

        has_some_changes = False
        for project_configuration in self.project_configurations:
            has_changes = ProjectUpdater.__edit_configuration(
                project_configuration=project_configuration,
                object_to_update=object_to_update,
            )
            if not has_changes:
                continue
            has_some_changes = True

        return has_some_changes

    @classmethod
    def __edit_configuration(
        cls, project_configuration: Path, object_to_update: dict[str, str]
    ):
        project_configuration_changes = cls.edit_configuration(
            project_configuration=project_configuration.read_text(),
            object_to_update=object_to_update,
        )
        if project_configuration_changes is None:
            return False

        project_configuration.write_text(project_configuration_changes)
        return True


class ProjectUpdaterException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
