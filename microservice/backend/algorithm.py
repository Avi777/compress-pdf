import math
import os

import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image


def get_dims(img, dpi):
    if isinstance(img, np.ndarray):
        img_h, img_w, _ = img.shape
    else:
        img_h, img_w = img.size
    r = img_h / img_w
    h, w = dpi * 8, math.ceil(dpi * 8 * r)
    if img_h > img_w:
        h, w = w, h
    return h, w


def compress_img(in_path, out_path, dpi):
    # cv2.resize is way faster than PIL resize
    img = cv2.imread(in_path)
    h, w = get_dims(img, dpi)
    img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
    status = cv2.imwrite(out_path, img, [cv2.IMWRITE_JPEG_QUALITY, 70])
    return status


def compress_pdf(in_path, out_path, dpi):
    images = convert_from_path(in_path)

    compressed_images = []
    for img in images:
        h, w = get_dims(img, dpi)
        img = img.resize((h, w), Image.ANTIALIAS)
        compressed_images.append(img.convert("RGB"))

    compressed_images[0].save(
        out_path, save_all=True, append_images=compressed_images[1:]
    )
    status = True

    return status


def compress(in_path, out_path="", dpi=100):
    if not out_path:
        outfile_name = "compressed-" + os.path.basename(in_path)
        out_path = os.path.join(os.path.dirname(in_path), outfile_name)

    _, file_extension = os.path.splitext(in_path)
    img_ext = [".jpg", ".png", ".jpeg"]

    if "pdf" in file_extension:
        status = compress_pdf(in_path, out_path, dpi)
    elif file_extension in img_ext:
        # jpg has better compression
        filename, file_extension = os.path.splitext(out_path)
        out_path = filename + ".jpg"
        status = compress_img(in_path, out_path, dpi)
    else:
        status = "Unsupported file type"

    res = {}
    res["status"] = status
    res["input_size"] = os.stat(in_path).st_size
    res["output_size"] = os.stat(out_path).st_size
    res["outfile"] = os.path.abspath(out_path)

    return res
