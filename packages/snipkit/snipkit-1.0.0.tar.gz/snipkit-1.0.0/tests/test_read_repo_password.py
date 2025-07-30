"""Tests around handling repositories which require authentication."""

from snipkit.prompt import read_repo_password


def test_click_invocation(mocker) -> None:
    """Test click function called correctly by snipkit.

    Test for password (hidden input) type invocation.
    """
    prompt = mocker.patch('rich.prompt.Prompt.ask')
    prompt.return_value = 'sekrit'

    assert read_repo_password('Password') == 'sekrit'

    prompt.assert_called_once_with('Password', password=True)
