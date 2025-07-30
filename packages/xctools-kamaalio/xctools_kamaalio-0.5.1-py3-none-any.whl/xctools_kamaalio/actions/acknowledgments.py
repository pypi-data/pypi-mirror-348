from dataclasses import asdict, dataclass
import glob
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import TypedDict


def acknowledgments():
    arguments = parse_arguments()

    packages_directory = get_packages_directory(project=arguments["project"])
    packages_licenses = get_packages_licenses(packages_directory=packages_directory)

    package_file_content = decode_package_file()
    packages = package_file_content_to_acknowledgments(
        package_file_content=package_file_content, packages_licenses=packages_licenses
    )

    contributors_list = subprocess.getoutput(
        'git log "--pretty=format:%an <%ae>"'
    ).splitlines()
    formatted_contributors = format_contributors(contributors_list=contributors_list)
    acknowledgements = Acknowledgements(
        packages=packages, contributors=formatted_contributors
    )

    output_path = Path(arguments["output"]) / "Acknowledgements.json"
    output_path.write_text(acknowledgements.to_json(indent=2))

    print("done writing acknowledgements ✨")


def format_contributors(contributors_list: list[str]):
    contributor_names_mapped_by_emails: dict[str, list[str]] = {}
    for contributor_entry in contributors_list:
        splitted_contributor_entry = contributor_entry.split("<")
        contributor_name = (
            "".join(splitted_contributor_entry[:-1])
            .strip()
            .replace("<", "")
            .replace(">", "")
        )
        email = splitted_contributor_entry[-1].strip().replace("<", "").replace(">", "")

        contributor_names_mapped_by_emails[email] = (
            contributor_names_mapped_by_emails.get(email, []) + [contributor_name]
        )

    contributors: list[Contributor] = []
    for email, contributor_names in contributor_names_mapped_by_emails.items():
        longest_contributor_name = ""

        for contributor_name in contributor_names:
            if contributor_name == "kamaal111" or contributor_name == "Kamaal":
                contributor_name = "Kamaal Farah"
            if len(contributor_name) > len(longest_contributor_name):
                longest_contributor_name = contributor_name

        contributors.append(
            Contributor(
                name=longest_contributor_name,
                email=email,
                contributions=len(contributor_names),
            )
        )

    merged_contributors: list[Contributor] = []
    for contributor in contributors:
        contributor_first_names_names = map(
            lambda contributor: contributor.first_name, merged_contributors
        )
        if contributor.first_name in contributor_first_names_names:
            for index, merged_author in enumerate(merged_contributors):
                first_name_is_the_same = (
                    contributor.first_name == merged_author.first_name
                )
                name_is_the_same = contributor.name == merged_author.name

                one_of_authors_has_just_a_single_name = (
                    contributor.has_just_a_single_name
                    or merged_author.has_just_a_single_name
                ) and len(contributor.name_components) != len(
                    merged_author.name_components
                )

                if first_name_is_the_same and (
                    one_of_authors_has_just_a_single_name or name_is_the_same
                ):
                    if len(contributor.name) > len(merged_author.name):
                        longest_author_name = contributor.name
                    else:
                        longest_author_name = merged_author.name

                    merged_contributors[index] = Contributor(
                        name=longest_author_name,
                        email=None,
                        contributions=contributor.contributions
                        + merged_author.contributions,
                    )
        else:
            contributor.email = None
            merged_contributors.append(contributor)

    return sorted(
        sorted(merged_contributors, key=lambda contributor: contributor.name),
        key=lambda contributor: contributor.contributions,
        reverse=True,
    )


def parse_arguments():
    arguments: Arguments = {}

    skip_next_value = False
    for index, arg in enumerate(sys.argv[1:]):
        if skip_next_value:
            skip_next_value = False
            continue

        def get_next_value():
            if index + 1 < len(sys.argv):
                nonlocal skip_next_value
                skip_next_value = True

                return sys.argv[index + 2]

        if arg == "--project" and (project := get_next_value()):
            arguments["project"] = project
        if arg == "--output" and (output := get_next_value()):
            arguments["output"] = output

    if arguments.get("project") is None:
        raise Exception("Please provide a project with the --project flag")

    if arguments.get("output") is None:
        raise Exception("Please provide a output path with the --output flag")

    return arguments


def get_path_from_root_ending_with(search_string: str) -> str | None:
    current_work_directory = os.getcwd()
    root_files = os.listdir(current_work_directory)

    for file in root_files:
        if file.endswith(search_string):
            return file


def get_packages_licenses(packages_directory: Path) -> dict[str, str]:
    """
    Extracts license information from packages in the specified directory.
    This function iterates through the subdirectories of the given `packages_directory`,
    looking for files containing the word "license" in their name. It reads the content
    of these files and maps each package name (subdirectory name) to its license text.
    Args:
        packages_directory (Path): The path to the directory containing package subdirectories.
    Returns:
        package_licenses (dict[str, str]): A dictionary where the keys are package names and the
        values are the corresponding license texts.
    """

    assert packages_directory.is_dir()

    licenses: dict[str, str] = {}
    for content_path in packages_directory.iterdir():
        if not content_path.is_dir():
            continue

        for package_path in content_path.iterdir():
            if not package_path.is_file() or "license" not in package_path.name.lower():
                continue

            licenses[content_path.name] = package_path.read_text()

    return licenses


def package_file_content_to_acknowledgments(
    package_file_content: "PackageFileContent", packages_licenses: dict[str, str]
):
    packages: list[AcknowledgementPackage] = []
    if package_object := package_file_content.get("object"):
        for pin in package_object["pins"]:
            package_name = pin["package"]
            url = pin["repositoryURL"]
            if url.endswith(".git"):
                url = url[:-4]

            author = url.split("/")[-2]

            acknowledgement = AcknowledgementPackage(
                name=package_name,
                url=url,
                author=author,
                license=packages_licenses.get(package_name),
            )
            packages.append(acknowledgement)
    else:
        for pin in package_file_content["pins"]:
            url = pin["location"]
            if url.endswith(".git"):
                url = url[:-4]

            url_split_by_separator = url.split("/")
            package_name = url_split_by_separator[-1]
            author = url_split_by_separator[-2]
            acknowledgement = AcknowledgementPackage(
                name=package_name,
                url=url,
                author=author,
                license=packages_licenses.get(package_name),
            )
            packages.append(acknowledgement)

    return packages


def decode_package_file() -> "PackageFileContent":
    if workspace_path := get_path_from_root_ending_with(search_string=".xcworkspace"):
        path = Path(workspace_path) / "xcshareddata" / "swiftpm" / "Package.resolved"
        return json.loads(path.read_text())

    raise Exception("Workspace not found at root")


def get_xcode_derived_data_base() -> Path:
    try:
        out = (
            subprocess.check_output(
                [
                    "defaults",
                    "read",
                    "com.apple.dt.Xcode",
                    "IDECustomDerivedDataLocation",
                ],
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
    except subprocess.CalledProcessError:
        out = ""

    if not out:
        return Path.home() / "Library/Developer/Xcode/DerivedData"

    return Path(os.path.expanduser(out))


def find_derived_data_for_project(project_name: str) -> Path:
    base = get_xcode_derived_data_base()
    pattern = str(base / f"{project_name}-*")
    matches = glob.glob(pattern)
    if not matches:
        raise FileNotFoundError(
            f"No DerivedData folder matching '{project_name}-*' in {base}"
        )

    matches.sort(key=lambda p: Path(p).stat().st_mtime, reverse=True)

    return Path(matches[0])


def get_packages_directory(project: str):
    project_path = get_path_from_root_ending_with(search_string=".xcodeproj")
    if project_path is None:
        raise FileNotFoundError("Project not found at root")

    derived_data_base = find_derived_data_for_project(project_name=project)

    return derived_data_base / "SourcePackages/checkouts"


@dataclass
class Acknowledgements:
    packages: list["AcknowledgementPackage"]
    contributors: list["Contributor"]

    def to_dict(self):
        dictionary_to_return = {}
        for key, value in asdict(self).items():
            dictionary_to_return[key] = value
        return dictionary_to_return

    def to_json(self, indent: int | None = None):
        return json.dumps(self.to_dict(), indent=indent)


@dataclass
class Contributor:
    name: str
    email: str | None
    contributions: int

    @property
    def first_name(self):
        return self.name_components[0]

    @property
    def name_components(self):
        return self.name.split(" ")

    @property
    def has_just_a_single_name(self):
        return len(self.name_components) == 1


@dataclass
class AcknowledgementPackage:
    name: str
    url: str
    author: str | None
    license: str | None


class Arguments(TypedDict):
    project: str
    output: str


class PackageFileContentObjectPinState(TypedDict):
    branch: str | None
    revision: str
    version: str | None


class PackageFileContentObjectPin(TypedDict):
    package: str
    repositoryURL: str
    state: PackageFileContentObjectPinState


class PackageFileContentObject(TypedDict):
    pins: list[PackageFileContentObjectPin]


class PackageFileContentPin(TypedDict):
    identity: str
    kind: str
    location: str
    state: PackageFileContentObjectPinState


class PackageFileContent(TypedDict):
    version: int
    object: PackageFileContentObject | None
    pins: list[PackageFileContentPin] | None
