"""Collection of tests around repository type identification."""

import pytest

from snipkit import exceptions, vcs


@pytest.mark.parametrize(
    'repo_url, exp_repo_type, exp_repo_url',
    [
        (
            'git+https://github.com/pytest-dev/snipkit-pytest-plugin.git',
            'git',
            'https://github.com/pytest-dev/snipkit-pytest-plugin.git',
        ),
        (
            'hg+https://bitbucket.org/foo/bar.hg',
            'hg',
            'https://bitbucket.org/foo/bar.hg',
        ),
        (
            'https://github.com/pytest-dev/snipkit-pytest-plugin.git',
            'git',
            'https://github.com/pytest-dev/snipkit-pytest-plugin.git',
        ),
        ('https://bitbucket.org/foo/bar.hg', 'hg', 'https://bitbucket.org/foo/bar.hg'),
        (
            'https://github.com/khulnasoft/snipkit.git',
            'git',
            'https://github.com/khulnasoft/snipkit.git',
        ),
        (
            'https://github.com/khulnasoft/snipkit',
            'git',
            'https://github.com/khulnasoft/snipkit',
        ),
        (
            'git@gitorious.org:snipkit-gitorious/snipkit-gitorious.git',
            'git',
            'git@gitorious.org:snipkit-gitorious/snipkit-gitorious.git',
        ),
        (
            'https://khulnasoft@bitbucket.org/khulnasoft/snipkit-bitbucket',
            'hg',
            'https://khulnasoft@bitbucket.org/khulnasoft/snipkit-bitbucket',
        ),
    ],
)
def test_identify_known_repo(repo_url, exp_repo_type, exp_repo_url) -> None:
    """Verify different correct repositories url syntax is correctly transformed."""
    assert vcs.identify_repo(repo_url) == (exp_repo_type, exp_repo_url)


@pytest.fixture(
    params=[
        'foo+git',  # uses explicit identifier with 'git' in the wrong place
        'foo+hg',  # uses explicit identifier with 'hg' in the wrong place
        'foo+bar',  # uses explicit identifier with neither 'git' nor 'hg'
        'foobar',  # no identifier but neither 'git' nor 'bitbucket' in url
        'http://norepotypespecified.com',
    ]
)
def unknown_repo_type_url(request):
    """Fixture. Return wrong formatted repository url."""
    return request.param


def test_identify_raise_on_unknown_repo(unknown_repo_type_url) -> None:
    """Verify different incorrect repositories url syntax trigger error raising."""
    with pytest.raises(exceptions.UnknownRepoType):
        vcs.identify_repo(unknown_repo_type_url)
