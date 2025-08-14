from __future__ import annotations
import argparse
from pathlib import Path
import sys
from .converter import image_to_ascii_string

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Convert an image to ASCII art (NumPy + Pillow).")
    p.add_argument("image", help="Path to input image (jpg/png/webp/etc.)")
    p.add_argument("-w", "--width", type=int, default=100, help="Output width in characters (default: 100)")
    p.add_argument("-o", "--out", type=str, default=None, help="Optional path to save ASCII as a .txt file")
    p.add_argument("--invert", action="store_true", help="Invert brightness mapping (light↔dark)")
    p.add_argument("--charset", type=str, default="@%#*+=-:. ", help="Characters dark→light (quote the string)")
    return p.parse_args()

def main() -> None:
    args = parse_args()
    if args.width < 1:
        print("Error: --width must be >= 1", file=sys.stderr)
        sys.exit(2)
    try:
        ascii_art = image_to_ascii_string(
            args.image, width=args.width, charset=args.charset, invert=args.invert
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(ascii_art)
    if args.out:
        out_path = Path(args.out)
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(ascii_art, encoding="utf-8")
            print(f"\nSaved to: {out_path.resolve()}", file=sys.stderr)
        except Exception as e:
            print(f"Warning: could not save to '{args.out}': {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
