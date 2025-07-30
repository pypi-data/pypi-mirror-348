# SPDX-FileCopyrightText: 2025 German Aerospace Center <amiris@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0
import logging
import os
from pathlib import Path
from typing import List

from amirispy.source.exception import AMIRISError
from amirispy.source.logs import log_error

_CSV_FILE_ENDING = ".csv"

_ERR_NOT_A_FOLDER = "Given Path '{}' is not a directory."
_ERR_MISSING_FOLDER = "Specified directory '{}' is missing."
_ERR_NO_ACCESS = "No writing permission to directory '{}'."

_WARN_NOT_EMPTY = "Folder '{}' is not empty - overriding files."


def get_all_csv_files_in_folder_except(folder: Path, exceptions: List[str] = None) -> List[Path]:
    """
    Find all csv files in a folder that can optionally ignore a files with a given file name

    Args:
        folder: to search for csv files - file ending is **not** case-sensitive
        exceptions: optional, files names (without file ending) listed here will be ignored - **not** case-sensitive

    Returns:
        Full file Paths for files ending with ".csv" not listed in exceptions

    Raises:
        AMIRISError: if folder is missing; logged with level "ERROR"
    """
    if not folder.is_dir():
        raise log_error(AMIRISError(_ERR_MISSING_FOLDER.format(folder)))

    if exceptions is None:
        exceptions = list()
    exceptions = [item.upper() for item in exceptions]
    all_csvs = [file for file in folder.glob(f"*{_CSV_FILE_ENDING}")]
    return [file for file in all_csvs if file.stem not in exceptions]


def ensure_folder_exists(path: Path) -> None:
    """
    Returns Path to a directory and creates the folder if required.
    If given Path is an existing folder: does nothing, else creates new folder (including parent folders)

    Args:
        path: to check and create if not existing

    Raises:
        AMIRISError: if path not found or an existing file; logged with level "ERROR"
    """
    try:
        if path.is_file():
            raise log_error(AMIRISError(_ERR_NOT_A_FOLDER.format(path)))
        if not path.is_dir():
            path.mkdir(parents=True)
    except FileNotFoundError:
        raise log_error(AMIRISError(_ERR_NOT_A_FOLDER.format(path)))


def check_if_write_access(path: Path) -> None:
    """
    Checks writing access in given `path` by writing and deleting a temporary file

    Args:
        path: to check if writing access

    Raises:
        AMIRISError: if no writing access in given path; logged with level "ERROR"
    """
    try:
        tmp_file_name = Path(path, "amirispy_write_access_test_file")
        file = open(tmp_file_name, "w")
        file.close()
        os.remove(tmp_file_name)
    except (OSError, IOError):
        raise log_error(AMIRISError(_ERR_NO_ACCESS.format(path)))


def warn_if_not_empty(folder: Path) -> None:
    """
    Logs a warning if given folder is not empty

    Args:
        folder: to check for files
    """
    if list(folder.glob("*")):
        logging.warning(_WARN_NOT_EMPTY.format(folder))
