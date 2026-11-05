#!/usr/bin/env python3
"""Optimize oversized cover copies in a prepared deployment directory.

Originals in the repository are never modified. Requires Pillow.
"""
import argparse
import io
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 100_000
MAX_SIZE = (600, 900)


def optimize_cover(path):
    """Replace an oversized staged JPEG only when the result is smaller."""
    original_size = path.stat().st_size
    if original_size <= MAX_BYTES:
        return original_size, original_size
    with Image.open(path) as image:
        image = ImageOps.exif_transpose(image).convert('RGB')
        image.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=82, optimize=True, progressive=True)
    optimized = output.getvalue()
    if len(optimized) < original_size:
        path.write_bytes(optimized)
        return original_size, len(optimized)
    return original_size, original_size


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('site_dir', type=Path, help='Prepared deployment directory, not the source repo')
    args = parser.parse_args()
    site = args.site_dir.resolve()
    covers = site / 'assets' / 'covers'
    if covers.resolve() == (ROOT / 'assets' / 'covers').resolve():
        parser.error('Refusing to modify the original cover directory')
    if not covers.is_dir():
        parser.error(f'Cover directory not found: {covers}')
    before = after = changed = 0
    for path in sorted(covers.glob('*.jpg')):
        old, new = optimize_cover(path)
        before += old
        after += new
        changed += new < old
    print(f'Optimized {changed} covers: {before:,} -> {after:,} bytes (all staged JPEG covers).')


if __name__ == '__main__':
    main()
