"""pytest fixtures for testing snipkit's replay feature."""

import pytest


@pytest.fixture
def context():
    """Fixture to return a valid context as known from a snipkit.json."""
    return {
        'snipkit': {
            'email': 'raphael@hackebrot.de',
            'full_name': 'Raphael Pierzina',
            'github_username': 'hackebrot',
            'version': '0.1.0',
        }
    }


@pytest.fixture
def replay_test_dir() -> str:
    """Fixture to test directory."""
    return 'tests/test-replay/'


@pytest.fixture
def mock_user_config(mocker):
    """Fixture to mock user config."""
    return mocker.patch('snipkit.main.get_user_config')
