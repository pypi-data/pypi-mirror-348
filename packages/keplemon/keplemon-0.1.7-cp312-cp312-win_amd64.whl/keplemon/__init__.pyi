# flake8: noqa
from pathlib import Path

def get_thread_count() -> int:
    """
    Returns:
        Number of cores allocated for use by KepLemon
    """
    ...

def set_thread_count(n: int) -> None:
    """
    Set the number of cores allocated for use by KepLemon

    !!! warning
        This function must be called before any other functions in the library

    Args:
        n: Number of cores to allocate
    """
    ...

#: Path to the time constants file
TIME_CONSTANTS_PATH: Path
"""
Path to the default time constants file required by the SAAL binaries

!!! warning
    This path should never be modified and is only exposed to allow inspection of current data.
"""
