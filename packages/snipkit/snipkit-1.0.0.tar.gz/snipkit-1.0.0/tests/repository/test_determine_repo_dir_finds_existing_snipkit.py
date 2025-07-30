"""Tests around detection whether snipkit templates are cached locally."""

import os
from pathlib import Path

import pytest

from snipkit import repository


@pytest.fixture
def template() -> str:
    """Fixture. Return simple string as template name."""
    return 'snipkit-pytest-plugin'


@pytest.fixture
def cloned_snipkit_path(user_config_data, template):
    """Fixture. Create fake project directory in special user folder."""
    snipkits_dir = user_config_data['snipkits_dir']

    cloned_template_path = os.path.join(snipkits_dir, template)
    os.mkdir(cloned_template_path)

    Path(cloned_template_path, "snipkit.json").touch()  # creates file

    return cloned_template_path


def test_should_find_existing_snipkit(
    template, user_config_data, cloned_snipkit_path
) -> None:
    """
    Should find folder created by `cloned_snipkit_path` and return it.

    This folder is considered like previously cloned project directory.
    """
    project_dir, cleanup = repository.determine_repo_dir(
        template=template,
        abbreviations={},
        clone_to_dir=user_config_data['snipkits_dir'],
        checkout=None,
        no_input=True,
    )

    assert cloned_snipkit_path == project_dir
    assert not cleanup
