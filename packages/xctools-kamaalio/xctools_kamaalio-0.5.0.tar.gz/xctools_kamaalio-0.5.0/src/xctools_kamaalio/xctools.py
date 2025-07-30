import json
import subprocess
from enum import Enum
from pathlib import Path
from typing import Literal

from xctools_kamaalio.project_updater import ProjectUpdater


class XcTools:
    @classmethod
    def export_archive(cls, archive_path: str, export_options: str):
        command = [
            "zsh",
            "-c",
            f'xcodebuild -exportArchive -archivePath "{archive_path}" -exportPath . '
            + f'-exportOptionsPlist "{export_options}"',
        ]
        cls.__run_command(command, "export-archive")

    @classmethod
    def archive(
        cls,
        scheme: str,
        configuration: Literal["Debug", "Release"],
        destination: str,
        sdk: Literal["macosx", "iphoneos"],
        archive_path: str,
        **kwargs,
    ):
        command = [
            "zsh",
            "-c",
            f'xcodebuild archive -scheme "{scheme}" -configuration {configuration} '
            + f'-destination "{destination}" -sdk {sdk} -archivePath "{archive_path}"',
        ]

        if project := kwargs.get("project"):
            command[-1] += f' -project "{project}"'
        elif workspace := kwargs.get("workspace"):
            command[-1] += f' -workspace "{workspace}"'
        else:
            raise XcToolsException("No workspace or project provided")

        cls.__run_command(command, "archive")

    @classmethod
    def upload(
        cls, target: Literal["ios", "macos"], file: str, username: str, password: str
    ):
        command = [
            "zsh",
            "-c",
            f'xcrun altool --upload-app -t {target} -f "{file}" -u {username} -p "{password}"',
        ]
        cls.__run_command(command, "upload")

    @staticmethod
    def bump_version(build_number: int | None, version_number: str | None):
        updater = ProjectUpdater()
        updater.bump_version(build_number=build_number, version_number=version_number)

    @classmethod
    def trust_swift_macros(cls, trust_file_path: str):
        cls.__trust_swift_package(
            trust_file_path=trust_file_path, file_type=TrustModuleTypes.MACROS
        )

    @classmethod
    def trust_swift_plugins(cls, trust_file_path: str):
        cls.__trust_swift_package(
            trust_file_path=trust_file_path, file_type=TrustModuleTypes.PLUGINS
        )

    @classmethod
    def test(
        cls,
        configuration: Literal["Debug", "Release"],
        scheme: str,
        destination: str,
        project: str | None,
        workspace: str | None,
    ):
        command = [
            "zsh",
            "-c",
            f'xcodebuild test -scheme "{scheme}" -configuration {configuration} -destination "{destination}"',
        ]

        if project:
            command[-1] += f' -project "{project}"'
        elif workspace:
            command[-1] += f' -workspace "{workspace}"'
        else:
            raise XcToolsException("No workspace or project provided")

        cls.__run_command(command, "test")

    @classmethod
    def build(
        cls,
        configuration: Literal["Debug", "Release"],
        scheme: str,
        destination: str,
        project: str | None,
        workspace: str | None,
    ):
        command = [
            "zsh",
            "-c",
            f'xcodebuild build -scheme "{scheme}" -configuration {configuration} -destination "{destination}"',
        ]

        if project:
            command[-1] += f' -project "{project}"'
        elif workspace:
            command[-1] += f' -workspace "{workspace}"'
        else:
            raise XcToolsException("No workspace or project provided")

        cls.__run_command(command, "build")

    @classmethod
    def __trust_swift_package(cls, trust_file_path: str, file_type: "TrustModuleTypes"):
        # TODO: DO THIS IN PYTHON INSTEAD
        cls.__run_command(
            command=["zsh", "-c", "mkdir -p ~/Library/org.swift.swiftpm/security/"],
            command_type="create security folder",
        )
        # TODO: DO THIS IN PYTHON INSTEAD
        cls.__run_command(
            command=[
                "zsh",
                "-c",
                f"rm -f ~/Library/org.swift.swiftpm/security/{file_type.name}.json",
            ],
            command_type="remove plugins file",
        )
        # TODO: DO THIS IN PYTHON INSTEAD
        cls.__run_command(
            command=[
                "zsh",
                "-c",
                f"touch ~/Library/org.swift.swiftpm/security/{file_type.name}.json",
            ],
            command_type="create plugins file",
        )
        trust_file = Path(trust_file_path)
        trust_file_content = json.loads(trust_file.read_text())
        assert isinstance(trust_file_content, list)
        trusted_modules = []
        for trust_config in trust_file_content:
            for i in range(0, len(trusted_modules)):
                trusted_plugin = trusted_modules[i]
                if trusted_plugin["packageIdentity"] == trust_config["packageIdentity"]:
                    trusted_modules[i] = trust_config
                    break
            else:
                trusted_modules.append(trust_config)
        for item in Path.home().glob("Library/org.swift.swiftpm"):
            trust_output_file = item / f"security/{file_type.name}.json"
            break
        else:
            raise XcToolsException("Output file not found")

        trust_output_file.write_text(json.dumps(trusted_modules, indent=2))

    @staticmethod
    def __run_command(command: list[str], command_type: str):
        process = subprocess.Popen(command)
        status = process.wait()
        if status != 0:
            raise XcToolsException(
                f"Failed {command_type} with status='{status}' on command='{command}'"
            )


class TrustModuleTypes(Enum):
    MACROS = "macros"
    PLUGINS = "plugins"


class XcToolsException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
