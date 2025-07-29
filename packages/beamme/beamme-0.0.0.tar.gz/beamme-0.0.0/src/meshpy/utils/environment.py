# The MIT License (MIT)
#
# Copyright (c) 2018-2025 MeshPy Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""Helper functions to interact with the MeshPy environment."""

import os as _os
from importlib.util import find_spec as _find_spec


def cubitpy_is_available() -> bool:
    """Check if CubitPy is installed.

    Returns:
        True if CubitPy is installed, False otherwise
    """

    if _find_spec("cubitpy") is None:
        return False
    return True


def fourcipp_is_available() -> bool:
    """Check if FourCIPP is installed.

    Returns:
        True if FourCIPP is installed, False otherwise
    """

    if _find_spec("fourcipp") is None:
        return False
    return True


def is_mybinder():
    """Check if the current environment is running on mybinder."""
    return "BINDER_LAUNCH_HOST" in _os.environ.keys()


def is_testing():
    """Check if the current environment is a pytest testing run."""
    return "PYTEST_CURRENT_TEST" in _os.environ


def get_env_variable(name, *, default="default_not_set"):
    """Return the value of an environment variable.

    Args
    ----
    name: str
        Name of the environment variable
    default:
        Value to be returned if the given named environment variable does
        not exist. If this is not set and the name is not in the env
        variables, then an error will be thrown.
    """
    if name in _os.environ.keys():
        return _os.environ[name]
    elif default == "default_not_set":
        raise ValueError(f"Environment variable {name} is not set")
    return default
