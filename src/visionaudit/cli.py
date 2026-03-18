from __future__ import annotations

import argparse
from pathlib import Path

from visionaudit.audit import apply_audit_rules
from visionaudit.config import AuditConfig
from visionaudit.report import build_summary, write_json_report
from visionaudit.scanner import scan_directory


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit image folders and generate a JSON report."
    )
    parser.add_argument("input", type=Path, help="Directory containing images")
    parser.add_argument("--output", type=Path, default=Path("visionaudit_report.json"))
    parser.add_argument("--min-width", type=int, default=256)
    parser.add_argument("--min-height", type=int, default=256)
    parser.add_argument("--max-file-size-bytes", type=int, default=10 * 1024 * 1024)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.input.exists() or not args.input.is_dir():
        parser.error(f"Input directory does not exist or is not a directory: {args.input}")

    config = AuditConfig(
        min_width=args.min_width,
        min_height=args.min_height,
        max_file_size_bytes=args.max_file_size_bytes,
    )

    records = scan_directory(args.input, config.allowed_extensions)
    records = apply_audit_rules(records, config)
    write_json_report(records, args.output)

    summary = build_summary(records)

    print(f"Scanned {summary.scanned_files} file(s)")
    print(f"Found {summary.issue_count} issue(s)")
    print(f"Errored files: {summary.errored_files}")
    print(f"Report written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())