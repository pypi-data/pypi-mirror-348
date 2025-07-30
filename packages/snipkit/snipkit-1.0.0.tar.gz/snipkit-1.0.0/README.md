# Snipkit

Create projects swiftly from **snipkits** (project templates) with this command-line utility. Ideal for generating Python package projects and more.

- [Documentation](https://snipkit.readthedocs.io)
- [GitHub](https://github.com/khulnasoft/snipkit)
- [PyPI](https://pypi.org/project/snipkit/)
- [License (BSD)](https://github.com/khulnasoft/snipkit/blob/main/LICENSE)

## Installation

Install snipkit using pip package manager:
```
# pipx is strongly recommended.
pipx install snipkit

# If pipx is not an option,
# you can install snipkit in your Python user directory.
python -m pip install --user snipkit
```

## Features

- **Cross-Platform:** Supports Windows, Mac, and Linux.
- **User-Friendly:** No Python knowledge required.
- **Versatile:** Compatible with Python 3.7 to 3.12.
- **Multi-Language Support:** Use templates in any language or markup format.

### For Users

#### Quick Start

The recommended way to use Snipkit as a command line utility is to run it with [`pipx`](https://pypa.github.io/pipx/), which can be installed with `pip install pipx`, but if you plan to use Snipkit programmatically, please run `pip install snipkit`.

**Use a GitHub template**

```bash
# You'll be prompted to enter values.
# Then it'll create your Python package in the current working directory,
# based on those values.
# For the sake of brevity, repos on GitHub can just use the 'gh' prefix
$ pipx run snipkit gh:khulnasoft/snipkit
```

**Use a local template**

```bash
$ pipx run snipkit snipkit-pypackage/
```

**Use it from Python**

```py
from snipkit.main import snipkit

# Create project from the snipkit-pypackage/ template
snipkit('snipkit-pypackage/')

# Create project from the snipkit-pypackage.git repo template
snipkit('gh:audreyfeldroy//snipkit-pypackage.git')
```

#### Detailed Usage

- Generate projects from local or remote templates.
- Customize projects with `snipkit.json` prompts.
- Utilize pre-prompt, pre- and post-generate hooks.

[Learn More](https://snipkit.readthedocs.io/en/latest/usage.html)

### For Template Creators

- Utilize unlimited directory nesting.
- Employ Jinja2 for all templating needs.
- Define template variables easily with `snipkit.json`.

[Learn More](https://snipkit.readthedocs.io/en/latest/tutorials/)

## Available Templates

Discover a variety of ready-to-use templates on [GitHub](https://github.com/search?q=snipkit&type=Repositories).