"""Safe tar extraction compatible with Python versions before 3.12."""

from __future__ import annotations

import inspect
import shutil
import tarfile
from pathlib import Path


class UnsafeArchiveError(RuntimeError):
    """Raised when an archive member cannot be extracted as ordinary data."""


def _safe_destination(root: Path, member_name: str) -> Path:
    if not member_name or "\x00" in member_name:
        raise UnsafeArchiveError("archive contains an empty or invalid member name")
    relative = Path(member_name)
    if relative.is_absolute() or ".." in relative.parts:
        raise UnsafeArchiveError(f"archive member escapes destination: {member_name!r}")
    destination = (root / relative).resolve(strict=False)
    if destination != root and root not in destination.parents:
        raise UnsafeArchiveError(f"archive member escapes destination: {member_name!r}")
    return destination


def _extract_regular_data(archive: tarfile.TarFile, destination: Path) -> None:
    """Conservative equivalent of the modern tarfile data filter."""

    root = destination.resolve()
    root.mkdir(parents=True, exist_ok=True)
    for member in archive.getmembers():
        target = _safe_destination(root, member.name)
        if member.isdir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        if not member.isfile():
            raise UnsafeArchiveError(
                f"archive member is not a regular file or directory: {member.name!r}"
            )
        target.parent.mkdir(parents=True, exist_ok=True)
        # Re-resolve after creating parents so pre-existing symlinks cannot
        # redirect the write outside the extraction root.
        target = _safe_destination(root, member.name)
        source = archive.extractfile(member)
        if source is None:
            raise UnsafeArchiveError(f"cannot read archive member: {member.name!r}")
        with source, target.open("wb") as output:
            shutil.copyfileobj(source, output)
        target.chmod(0o600)


def extract_data(archive: tarfile.TarFile, destination: Path) -> None:
    """Use the standard data filter when available, otherwise its safe subset."""

    parameters = inspect.signature(tarfile.TarFile.extractall).parameters
    if "filter" in parameters:
        archive.extractall(destination, filter="data")
        return
    _extract_regular_data(archive, destination)
