#!/usr/bin/env python

# This is intended to be run with the 'skel' branch of some other repo checked
# out.

import configparser
import re
from pathlib import Path
from typing import Match

THIS_DIR = Path(__file__).absolute().parent
TEMPLATE_DIR = THIS_DIR / "templates"

# This is very simplistic...
VARIABLE_RE = re.compile(r"(?<!{){(\w+)}")
VARS_FILENAME = ".vars.ini"


def variable_format(tmpl: str, **kwargs: str) -> str:
    """
    This is similar to string.format but uses the regex above.

    This means that '{ foo }' is not an interpolation, nor is '{{foo}}', but we
    also don't get '!r' suffix for free.  Maybe someday.
    """

    def replace(match: Match[str]) -> str:
        g = match.group(1)
        if g in kwargs:
            return kwargs[g]
        return match.group(0)

    return VARIABLE_RE.sub(replace, tmpl)


def is_template_file(filepath: Path) -> bool:
    return (
        filepath.suffix == 'in'
        or filepath.name == '__init__.py'
    )


def main() -> None:
    # In case we've answered anything before, attempt load.
    parser = configparser.RawConfigParser()
    parser.read([VARS_FILENAME])
    if "vars" not in parser:
        parser.add_section("vars")

    for template_path in TEMPLATE_DIR.glob('**/*'):
        dirpath = template_path.parent

        if is_template_file(template_path):
            with template_path.open("r") as f:
                data = f.read()

            variables = list()
            variables.extend(VARIABLE_RE.findall(data))
            variables.extend(VARIABLE_RE.findall(str(template_path)))

            for v in variables:
                if v not in parser["vars"]:
                    parser["vars"][v] = input(f"Value for {v}? ").strip()
                    with open(VARS_FILENAME, "w") as f:
                        parser.write(f)

            interpolated_data = variable_format(data, **parser["vars"])

            local_path = (dirpath / template_path.with_suffix('')).relative_to(TEMPLATE_DIR)
            local_path = Path(variable_format(str(local_path), **parser["vars"]))

            if local_path.exists():
                with local_path.open("r") as f:
                    existing_data = f.read()
                if existing_data == interpolated_data:
                    print(f"Unchanged {local_path}")
                    continue

            print(f"Writing {local_path}")
            local_path.parent.mkdir(parents=True, exist_ok=True)
            with local_path.open("w") as f:
                f.write(interpolated_data)


if __name__ == "__main__":
    main()
