"""Allow snipkit to be executable through `python -m snipkit`."""

from snipkit.cli import main

if __name__ == "__main__":
    main(prog_name="snipkit")
