from __future__ import annotations

import json
from pathlib import Path

from visionaudit.models import AuditSummary, ImageRecord


def build_summary(records: list[ImageRecord]) -> AuditSummary:
    issue_count = sum(len(record.issues) for record in records)
    errored_files = sum(
        1
        for record in records
        if any(issue.severity == "error" for issue in record.issues)
    )
    return AuditSummary(
        scanned_files=len(records),
        issue_count=issue_count,
        errored_files=errored_files,
    )


def records_to_dict(records: list[ImageRecord]) -> dict:
    summary = build_summary(records)
    return {
        "summary": {
            "scanned_files": summary.scanned_files,
            "issue_count": summary.issue_count,
            "errored_files": summary.errored_files,
        },
        "files": [
            {
                "path": str(record.path),
                "file_size_bytes": record.file_size_bytes,
                "width": record.width,
                "height": record.height,
                "resolution": record.resolution,
                "format": record.format,
                "issues": [
                    {
                        "code": issue.code,
                        "message": issue.message,
                        "severity": issue.severity,
                        "details": issue.details,
                    }
                    for issue in record.issues
                ],
            }
            for record in records
        ],
    }


def write_json_report(records: list[ImageRecord], output_path: Path) -> None:
    payload = records_to_dict(records)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")