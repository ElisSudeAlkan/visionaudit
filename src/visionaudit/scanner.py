from __future__ import annotations

from pathlib import Path

from PIL import Image, UnidentifiedImageError

from visionaudit.models import AuditIssue, ImageRecord


def discover_images(root: Path, allowed_extensions: set[str]) -> list[Path]:
    paths: list[Path] = []
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in allowed_extensions:
            paths.append(path)
    return sorted(paths)


def scan_image(path: Path) -> ImageRecord:
    record = ImageRecord(path=path, file_size_bytes=path.stat().st_size)

    try:
        with Image.open(path) as img:
            record.width, record.height = img.size
            record.format = img.format
    except (UnidentifiedImageError, OSError) as exc:
        record.issues.append(
            AuditIssue(
                code="corrupt_or_unreadable",
                message="Image could not be opened.",
                severity="error",
                details={"error": str(exc)},
            )
        )

    return record


def scan_directory(root: Path, allowed_extensions: set[str]) -> list[ImageRecord]:
    return [scan_image(path) for path in discover_images(root, allowed_extensions)]