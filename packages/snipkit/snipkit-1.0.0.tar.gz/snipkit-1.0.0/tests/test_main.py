"""Collection of tests around snipkit's replay feature."""

from snipkit.main import snipkit


def test_original_snipkit_options_preserved_in__snipkit(
    monkeypatch,
    mocker,
    user_config_file,
) -> None:
    """Preserve original context options.

    Tests you can access the original context options via
    `context['_snipkit']`.
    """
    monkeypatch.chdir('tests/fake-repo-tmpl-_snipkit')
    mock_generate_files = mocker.patch('snipkit.main.generate_files')
    snipkit(
        '.',
        no_input=True,
        replay=False,
        config_file=user_config_file,
    )
    assert mock_generate_files.call_args[1]['context']['_snipkit'][
        'test_list'
    ] == [1, 2, 3, 4]
    assert mock_generate_files.call_args[1]['context']['_snipkit'][
        'test_dict'
    ] == {"foo": "bar"}


def test_replay_dump_template_name(
    monkeypatch, mocker, user_config_data, user_config_file
) -> None:
    """Check that replay_dump is called with a valid template_name.

    Template name must not be a relative path.

    Otherwise files such as ``..json`` are created, which are not just cryptic
    but also later mistaken for replay files of other templates if invoked with
    '.' and '--replay'.

    Change the current working directory temporarily to 'tests/fake-repo-tmpl'
    for this test and call snipkit with '.' for the target template.
    """
    monkeypatch.chdir('tests/fake-repo-tmpl')

    mock_replay_dump = mocker.patch('snipkit.main.dump')
    mocker.patch('snipkit.main.generate_files')

    snipkit(
        '.',
        no_input=True,
        replay=False,
        config_file=user_config_file,
    )

    mock_replay_dump.assert_called_once_with(
        user_config_data['replay_dir'],
        'fake-repo-tmpl',
        mocker.ANY,
    )


def test_replay_load_template_name(
    monkeypatch, mocker, user_config_data, user_config_file
) -> None:
    """Check that replay_load is called correctly.

    Calls require valid template_name that is not a relative path.

    Change the current working directory temporarily to 'tests/fake-repo-tmpl'
    for this test and call snipkit with '.' for the target template.
    """
    monkeypatch.chdir('tests/fake-repo-tmpl')

    mock_replay_load = mocker.patch('snipkit.main.load')
    mocker.patch('snipkit.main.generate_context').return_value = {
        'snipkit': {}
    }
    mocker.patch('snipkit.main.generate_files')
    mocker.patch('snipkit.main.dump')

    snipkit(
        '.',
        replay=True,
        config_file=user_config_file,
    )

    mock_replay_load.assert_called_once_with(
        user_config_data['replay_dir'],
        'fake-repo-tmpl',
    )


def test_custom_replay_file(monkeypatch, mocker, user_config_file) -> None:
    """Check that reply.load is called with the custom replay_file."""
    monkeypatch.chdir('tests/fake-repo-tmpl')

    mock_replay_load = mocker.patch('snipkit.main.load')
    mocker.patch('snipkit.main.generate_context').return_value = {
        'snipkit': {}
    }
    mocker.patch('snipkit.main.generate_files')
    mocker.patch('snipkit.main.dump')

    snipkit(
        '.',
        replay='./custom-replay-file',
        config_file=user_config_file,
    )

    mock_replay_load.assert_called_once_with(
        '.',
        'custom-replay-file',
    )
