from pathlib import Path

from visionaudit.audit import apply_audit_rules
from visionaudit.config import AuditConfig
from visionaudit.models import ImageRecord


def test_apply_audit_rules_flags_small_dimensions() -> None:
    record = ImageRecord(
        path=Path("tiny.png"),
        file_size_bytes=100,
        width=100,
        height=120,
        format="PNG",
    )
    config = AuditConfig(min_width=256, min_height=256)

    results = apply_audit_rules([record], config)

    codes = {issue.code for issue in results[0].issues}
    assert "width_too_small" in codes
    assert "height_too_small" in codes