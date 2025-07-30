"""snipkit distutils configuration."""

from pathlib import Path

from setuptools import setup


def _get_version() -> str:
    """Read snipkit/VERSION.txt and return its contents."""
    path = Path("snipkit").resolve()
    version_file = path / "VERSION.txt"
    return version_file.read_text().strip()


version = _get_version()

readme = Path('README.md').read_text(encoding='utf-8')

requirements = [
    'binaryornot>=0.4.4',
    'Jinja2>=2.7,<4.0.0',
    'click>=7.0,<9.0.0',
    'pyyaml>=5.3.1',
    'python-slugify>=4.0.0',
    'requests>=2.23.0',
    'arrow',
    'rich',
]

setup(
    name='snipkit',
    version=version,
    description=(
        'A command-line utility that creates projects from project '
        'templates, e.g. creating a Python package project from a '
        'Python package project template.'
    ),
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Md Sulaiman',
    author_email='dev.sulaiman@icloud.com',
    url='https://github.com/khulnasoft/snipkit',
    project_urls={
        "Documentation": "https://snipkit.readthedocs.io",
        "Issues": "https://github.com/khulnasoft/snipkit/issues",
    },
    packages=['snipkit'],
    package_dir={'snipkit': 'snipkit'},
    entry_points={'console_scripts': ['snipkit = snipkit.__main__:main']},
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=requirements,
    license='BSD',
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
    keywords=[
        "snipkit",
        "Python",
        "projects",
        "project templates",
        "Jinja2",
        "skeleton",
        "scaffolding",
        "project directory",
        "package",
        "packaging",
    ],
)
