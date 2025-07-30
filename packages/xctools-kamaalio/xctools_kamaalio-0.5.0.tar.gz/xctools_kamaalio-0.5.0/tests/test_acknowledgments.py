import pytest
from xctools_kamaalio.actions.acknowledgments import Contributor, format_contributors


@pytest.mark.parametrize(
    "contributors_list_input, expected_contributors",
    [
        (
            [
                "John <john@email.com>",
                "Kamaal <kamaal@email.com>",
                "John Smith <john.smith@email.com>",
                "Kamaal Farah <kamaal.farah@email.com>",
            ],
            [
                Contributor(name="John Smith", email=None, contributions=2),
                Contributor(name="Kamaal Farah", email=None, contributions=2),
            ],
        ),
        (
            [
                "John <john@email.com>",
                "John Smith <john.smith@email.com>",
                "Kamaal Farah <kamaal.farah@email.com>",
                "Kamaal <kamaal@email.com>",
            ],
            [
                Contributor(name="John Smith", email=None, contributions=2),
                Contributor(name="Kamaal Farah", email=None, contributions=2),
            ],
        ),
        (
            [
                "Kent Clark <kent.clark@email.com>",
                "John <john@email.com>",
                "John Smith <john.smith@email.com>",
                "Kamaal Farah <kamaal.farah@email.com>",
                "Kamaal <kamaal@email.com>",
            ],
            [
                Contributor(name="John Smith", email=None, contributions=2),
                Contributor(name="Kamaal Farah", email=None, contributions=2),
                Contributor(name="Kent Clark", email=None, contributions=1),
            ],
        ),
    ],
)
def test_format_contributors(contributors_list_input, expected_contributors):
    contributors = format_contributors(contributors_list_input)

    assert contributors == expected_contributors
