"""Test snipkit invocation with nested configuration structure."""

from pathlib import Path

import pytest

from snipkit import main


@pytest.mark.parametrize(
    "template_dir,output_dir",
    [
        ["fake-nested-templates", "fake-project"],
        ["fake-nested-templates-old-style", "fake-package"],
    ],
)
def test_snipkit_nested_templates(
    mocker, template_dir: str, output_dir: str
) -> None:
    """Verify snipkit nested configuration files mechanism."""
    mock_generate_files = mocker.patch("snipkit.main.generate_files")
    main_dir = (Path("tests") / template_dir).resolve()
    main.snipkit(f"{main_dir}", no_input=True)
    expected = (Path(main_dir) / output_dir).resolve()
    assert mock_generate_files.call_args[1]["repo_dir"] == f"{expected}"
