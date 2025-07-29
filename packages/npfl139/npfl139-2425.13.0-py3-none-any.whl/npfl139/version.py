# This file is part of NPFL139 <http://github.com/ufal/npfl139/>.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

__version__ = "2425.13.0"


def require_version(required_version: str) -> None:
    required = required_version.split(".")
    assert len(required) <= 3, "Expected at most 3 version components"

    required = list(map(int, required))
    current = list(map(int, __version__.split(".")))

    assert current[:len(required)] >= required, (
        f"The npfl139>={required_version} is required, but found only {__version__}.\n"
        f"Please update the npfl139 package by running either:\n"
        f"- `VENV_DIR/bin/pip install --upgrade npfl139` when using a venv, or\n"
        f"- `python3 -m pip install --user --upgrade npfl139` otherwise.")
