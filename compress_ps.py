import math
import os
from pathlib import Path

import numpy as np
from pdf2image import convert_from_path
from PIL import Image


def get_dims(image, dpi=72):
    h, w = dpi * 8, math.ceil(dpi * 8 * math.sqrt(2))
    img_h, img_w = image.size
    if img_h > img_w:
        h, w = w, h
    return h, w


def compress(in_path, out_path, dpi):
    FILE_PATH = Path(in_path)
    images = convert_from_path(FILE_PATH)
    images_compressed = []
    for image in images:
        h, w = get_dims(image, dpi)
        image = image.resize((h, w), Image.ANTIALIAS)
        images_compressed.append(image.convert("RGB"))
    images_compressed[0].save(out_path, save_all=True, append_images=images_compressed[1:])


if __name__ == "__main__":
    from sys import argv

    in_path = argv[1]
    dpi = int(argv[3]) if len(argv) == 4 else 72

    filename = os.path.split(in_path)[-1]
    out_file = in_path.replace(
        filename, filename.split(".")[0] + f"-compressed-{dpi}.pdf"
    )

    out_path = argv[2] if len(argv) == 3 else out_file
    compress(in_path, out_path, dpi)
