"""Tests for `repository_has_snipkit_json` function."""

import pytest

from snipkit.repository import repository_has_snipkit_json


def test_valid_repository() -> None:
    """Validate correct response if `snipkit.json` file exist."""
    assert repository_has_snipkit_json('tests/fake-repo')


@pytest.mark.parametrize(
    'invalid_repository', (['tests/fake-repo-bad', 'tests/unknown-repo'])
)
def test_invalid_repository(invalid_repository) -> None:
    """Validate correct response if `snipkit.json` file not exist."""
    assert not repository_has_snipkit_json(invalid_repository)
