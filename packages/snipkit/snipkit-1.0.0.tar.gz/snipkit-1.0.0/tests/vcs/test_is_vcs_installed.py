"""Collection of tests around VCS detection."""

import pytest

from snipkit import vcs


@pytest.mark.parametrize(
    'which_return, result',
    [('', False), (None, False), (False, False), ('/usr/local/bin/git', True)],
)
def test_is_vcs_installed(mocker, which_return, result) -> None:
    """Verify `is_vcs_installed` function correctly handles `which` answer."""
    mocker.patch('snipkit.vcs.which', autospec=True, return_value=which_return)
    assert vcs.is_vcs_installed('git') == result
