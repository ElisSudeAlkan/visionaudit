from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class AuditConfig:
    min_width: int = 256
    min_height: int = 256
    max_file_size_bytes: int = 10 * 1024 * 1024
    allowed_extensions: set[str] = field(
        default_factory=lambda: {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}
    )