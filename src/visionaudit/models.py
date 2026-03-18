from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class AuditIssue:
    code: str
    message: str
    severity: str = "warning"
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ImageRecord:
    path: Path
    file_size_bytes: int
    width: int | None = None
    height: int | None = None
    format: str | None = None
    issues: list[AuditIssue] = field(default_factory=list)

    @property
    def resolution(self) -> str | None:
        if self.width is None or self.height is None:
            return None
        return f"{self.width}x{self.height}"


@dataclass(slots=True)
class AuditSummary:
    scanned_files: int
    issue_count: int
    errored_files: int