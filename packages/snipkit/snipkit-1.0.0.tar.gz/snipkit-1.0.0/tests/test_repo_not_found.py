"""Testing invalid snipkit template repositories."""

import pytest

from snipkit import exceptions, main


def test_should_raise_error_if_repo_does_not_exist() -> None:
    """Snipkit invocation with non-exist repository should raise error."""
    with pytest.raises(exceptions.RepositoryNotFound):
        main.snipkit('definitely-not-a-valid-repo-dir')
