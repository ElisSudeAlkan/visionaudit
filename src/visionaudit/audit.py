from __future__ import annotations

from visionaudit.config import AuditConfig
from visionaudit.models import AuditIssue, ImageRecord


def apply_audit_rules(records: list[ImageRecord], config: AuditConfig) -> list[ImageRecord]:
    for record in records:
        if record.width is not None and record.width < config.min_width:
            record.issues.append(
                AuditIssue(
                    code="width_too_small",
                    message=f"Image width is below minimum ({config.min_width}px).",
                    details={
                        "actual_width": record.width,
                        "min_width": config.min_width,
                    },
                )
            )

        if record.height is not None and record.height < config.min_height:
            record.issues.append(
                AuditIssue(
                    code="height_too_small",
                    message=f"Image height is below minimum ({config.min_height}px).",
                    details={
                        "actual_height": record.height,
                        "min_height": config.min_height,
                    },
                )
            )

        if record.file_size_bytes > config.max_file_size_bytes:
            record.issues.append(
                AuditIssue(
                    code="file_too_large",
                    message="Image file size exceeds configured maximum.",
                    details={
                        "actual_size_bytes": record.file_size_bytes,
                        "max_size_bytes": config.max_file_size_bytes,
                    },
                )
            )

    return records