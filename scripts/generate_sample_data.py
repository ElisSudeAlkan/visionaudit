from __future__ import annotations

from pathlib import Path

from PIL import Image


def make_tiny_image(output_dir: Path) -> Path:
    path = output_dir / "tiny.png"
    Image.new("RGB", (64, 64), color=(255, 0, 0)).save(path)
    return path


def make_corrupt_image(output_dir: Path) -> Path:
    path = output_dir / "corrupt.png"
    path.write_bytes(b"this is not a valid png file")
    return path


def make_large_image(output_dir: Path) -> Path:
    path = output_dir / "large_file.png"

    # Large enough to exceed a small max-file-size threshold in tests/CLI runs.
    # PNG can compress flat colors very well, so use varying pixel values.
    image = Image.new("RGB", (3000, 3000))
    pixels = image.load()

    for x in range(3000):
        for y in range(3000):
            pixels[x, y] = (
                (x * 7 + y * 3) % 256,
                (x * 5 + y * 11) % 256,
                (x * 13 + y * 17) % 256,
            )

    image.save(path)
    return path


def main() -> None:
    output_dir = Path("sample_data/images")
    output_dir.mkdir(parents=True, exist_ok=True)

    created = [
        make_tiny_image(output_dir),
        make_corrupt_image(output_dir),
        make_large_image(output_dir),
    ]

    print("Created sample files:")
    for path in created:
        print(f" - {path}")


if __name__ == "__main__":
    main()