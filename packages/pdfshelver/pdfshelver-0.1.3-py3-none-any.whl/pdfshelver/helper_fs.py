"""Helper filesystem functions for pdfshelver"""

import shutil
from pathlib import Path


def create_dir(dirname: str | Path) -> None:
    """Simple helper to create a directory and make sure it exists.
    Bails out if not possible."""
    dpath = Path(dirname)
    dpath.mkdir(parents=True, exist_ok=True)
    if not (dpath.exists() and dpath.is_dir()):
        raise RuntimeError(
            f"Could not create directory {dirname}, aborting.",
        )
    return


def copy_file(src: str | Path, dest: str | Path) -> str:
    """Simple helper to copy a file and make sure it exists.
    Throws RuntimeError if not possible."""

    # return value: signature now for later when implementing dest also allowed as directory

    spath = Path(src)
    dpath = Path(dest)
    # don't copy if both src and dest are the same file
    if dpath.is_dir():
        raise NotImplementedError(
            f"{dpath} should be a directory, aborting.",
        )
    if spath.is_file() and dpath.is_file() and spath.samefile(dpath):
        return str(dpath)

    if spath.is_file():
        tpath = dpath.with_name(f"{dpath.name}.tmp")  # bad, should use real tmp name
        resname: Path | str = shutil.copy2(spath, tpath)
        if not Path(resname).is_file():
            raise RuntimeError(
                f"Could not copy file {spath} to destination {dpath}, aborting.",
            )
        tpath.rename(dpath)
    else:
        raise RuntimeError(
            f"{src} must be a file, but it is not. Does it exist? Is it a directory?"
        )
    return str(dpath)
