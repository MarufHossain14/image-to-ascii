from __future__ import annotations
from pathlib import Path
from typing import Iterable
import numpy as np
from PIL import Image

CHAR_ASPECT = 0.55  # character cell height/width compensation

def _load_grayscale(image_path: str | Path) -> Image.Image:
    return Image.open(image_path).convert("L")

def _resize(img: Image.Image, width: int) -> Image.Image:
    w, h = img.size
    new_h = max(1, int((h / w) * width * CHAR_ASPECT))
    return img.resize((width, new_h))

def _map_pixels_to_chars(arr: np.ndarray, charset: Iterable[str], invert: bool) -> np.ndarray:
    chars = np.array(list(charset))
    if invert:
        chars = chars[::-1]
    idx = np.rint(arr.astype(np.float32) / 255 * (len(chars) - 1)).astype(int)
    return chars[idx]

def image_to_ascii_string(
    image_path: str | Path,
    width: int = 100,
    charset: str = "@%#*+=-:. ",
    invert: bool = False,
) -> str:
    img = _load_grayscale(image_path)
    img = _resize(img, width)
    arr = np.array(img, dtype=np.uint8)  # (H, W) 0..255
    ascii_arr = _map_pixels_to_chars(arr, charset, invert)
    lines = ["".join(row.tolist()) for row in ascii_arr]
    return "\n".join(lines)
