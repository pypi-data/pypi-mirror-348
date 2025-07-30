import sys

from kamaaalpy.lists import removed, find_index

from xctools_kamaalio.actions.acknowledgments import acknowledgments
from xctools_kamaalio.actions.upload import upload
from xctools_kamaalio.actions.archive import archive
from xctools_kamaalio.actions.bump_version import bump_version
from xctools_kamaalio.actions.export_archive import export_archive
from xctools_kamaalio.actions.trust_swift_plugins import trust_swift_plugins
from xctools_kamaalio.actions.trust_swift_macros import trust_swift_macros
from xctools_kamaalio.actions.test import test
from xctools_kamaalio.actions.build import build


MAPPED_ACTIONS = {
    "archive": archive,
    "upload": upload,
    "bump-version": bump_version,
    "export-archive": export_archive,
    "trust-swift-plugins": trust_swift_plugins,
    "trust-swift-macros": trust_swift_macros,
    "test": test,
    "build": build,
    "acknowledgments": acknowledgments,
}


def cli():
    action_index = find_index(sys.argv, lambda arg: arg in MAPPED_ACTIONS.keys())
    if action_index is None:
        raise CLIException("Invalid action provided")

    action = sys.argv[action_index]
    sys.argv = removed(sys.argv, action_index)

    MAPPED_ACTIONS[action]()


class CLIException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
