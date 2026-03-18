# VisionAudit

VisionAudit is an offline CLI tool for scanning image directories, applying simple audit rules, and generating structured JSON reports.

## Features

- Recursively scans image directories
- Extracts image metadata such as width, height, format, and file size
- Applies basic audit rules:
  - minimum width
  - minimum height
  - maximum file size
  - unreadable/corrupt image detection
- Writes a JSON report

## Installation

```bash
python -m pip install -r requirements.txt
python -m pip install -e .