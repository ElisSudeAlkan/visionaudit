import json
from pathlib import Path
from subprocess import run

from PIL import Image


def test_cli_generates_report(tmp_path: Path) -> None:
    input_dir = tmp_path / "images"
    input_dir.mkdir()

    Image.new("RGB", (300, 300)).save(input_dir / "ok.png")
    output_file = tmp_path / "report.json"

    result = run(
        [
            "python",
            "-m",
            "visionaudit.cli",
            str(input_dir),
            "--output",
            str(output_file),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert output_file.exists()

    payload = json.loads(output_file.read_text(encoding="utf-8"))
    assert payload["summary"]["scanned_files"] == 1