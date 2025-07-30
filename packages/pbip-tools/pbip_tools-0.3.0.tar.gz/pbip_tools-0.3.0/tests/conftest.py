"""Shared `pytest` fixtures."""

import shutil
import sys
from collections.abc import Callable, Iterable, Iterator
from pathlib import Path

import pytest

from pbip_tools.clean.clean_JSON import clean_json
from pbip_tools.smudge.smudge_JSON import smudge_json
from pbip_tools.type_aliases import JSONType, PathLike

tests_directory = Path(__file__).parent
json_files_list = list(tests_directory.glob("Sample PBIP Reports/**/*.json"))


@pytest.fixture(params=json_files_list, ids=str)
def json_files() -> list[Path]:
    """
    All JSON files from the sample Power BI report.

    These JSON files are globbed from the project directory and point to the files in
    the current project.
    """
    return json_files_list


@pytest.fixture
def temp_json_files(json_files: list[Path], tmp_path: Path) -> Iterable[Path]:
    """
    All JSON files from the sample Power BI report in a temporary directory.

    The JSON files are globbed from the project directory then copied to a temporary
    directory. The refer to a copy of the file and not the original project file.

    Returns
    -------
    Iterable[Path]
        A list or Iterable over the temporary JSON filepaths.
    """
    for file in json_files:
        shutil.copy2(file, tmp_path / file.name)
    return ((tmp_path / file.name).resolve() for file in json_files)


@pytest.fixture(params=json_files_list, ids=str)
def json_file(request: pytest.FixtureRequest) -> Path:
    """
    Return a single JSON file from the sample Power BI report.

    Returns
    -------
    Path
        Path to the JSON file in the test.
    """
    return request.param


@pytest.fixture
def json_from_file_str(json_file: Path) -> str:
    """
    Return the content of a test JSON file as a string.

    Returns
    -------
    str
        The contents of the test JSON file as a string.
    """
    return Path(json_file).read_text(encoding="UTF-8")


@pytest.fixture(
    params=[clean_json, smudge_json, lambda text: clean_json(text, indent=5)]
)
def filter_function(request: pytest.FixtureRequest) -> Callable[[JSONType], str]:
    """
    Fixture that provides either the `clean_json` or `smudge_json` function.

    This parameterized fixture will alternate between the two filter functions. This
    allows tests to apply both filters without duplicating test code.

    Returns
    -------
    Callable[[JSONType], str]
        The `clean_json` or `smudge_json` function.
    """
    return request.param


filter_func_cli_executable_params = ["json-clean", "json-smudge"]
pbip_tools_cli_executable_params = [
    "clean",
    "smudge",
    "clean --indent=13",
    "clean --sort-lists",
    "clean --indent=17 --sort-lists",
]
any_cli_executable_params = (
    filter_func_cli_executable_params + pbip_tools_cli_executable_params
)


@pytest.fixture(params=filter_func_cli_executable_params)
def filter_func_cli_executable(request: pytest.FixtureRequest) -> Iterable[PathLike]:
    """Return the executable to `json-clean` or `json-smudge`."""
    tool = request.param
    executable = Path(sys.executable).parent / tool

    return [executable]


@pytest.fixture(params=pbip_tools_cli_executable_params)
def pbip_tools_cli_executable(request: pytest.FixtureRequest) -> Iterable[str]:
    """
    Return `pbip-tools clean` or `pbip-tools smudge` as a list.

    Return either `pbip-tools clean` or `pbip-tools smudge` as a list ready to be
    processed by `subprocess.run`.
    """
    executable = Path(sys.executable).parent / "pbip-tools"
    subcommand = request.param.split()
    return list(map(str, [executable, *subcommand]))


@pytest.fixture(params=["filter_func_cli_executable", "pbip_tools_cli_executable"])
def any_cli_executable(
    request: pytest.FixtureRequest,
    filter_func_cli_executable: Iterable[PathLike],  # noqa: ARG001
    pbip_tools_cli_executable: Iterable[str],  # noqa: ARG001 (Unused function argument)
) -> Iterator[str]:
    """
    Return `json-clean`, `pbip-tools clean`, or smudge equivalents.

    Combine the fixtures `filter_func_cli_executable` and `pbip_tools_cli_executable` to
    yield all command combinations. The result will be appear like:
      - `["json-clean"]`
      - `["json-smudge"]`
      - `["pbip-tools", "clean"]`
      - `["pbip-tools", "smudge"]`
      - `["pbip-tools", "clean", "--indent=13"]`
      - `["pbip-tools", "clean", "--sort-lists"]`
      - `["pbip-tools", "clean", "--indent=17", "--sort-lists"]`
    This fixture is meant to be passed to `subprocess.run`.

    Notes
    -----
    Using `request.getfixturevalue` is kind of a hacky way to string together the two
    fixtures in the function signature.
    """
    return request.getfixturevalue(request.param)
