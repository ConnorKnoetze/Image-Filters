from PIL import Image
import os
import numpy as np
from flask import url_for

def do_duotone(image):
    orig = np.array(image)
    height, width = orig.shape[0], orig.shape[1]
    img = orig.astype(np.float32)

    # Normalize color stops to 0..1
    Cs = np.array([17, 18, 107], dtype=np.float32) / 255.0
    Ch = np.array([255, 172, 255], dtype=np.float32) / 255.0

    def lin(x):
        return (x / 255.0) ** 2.2

    def gam(x):
        return (x ** (1.0 / 2.2)) * 255.0

    has_alpha = orig.ndim == 3 and orig.shape[2] == 4

    out = orig.copy()

    for h in range(height):
        for w in range(width):
            r, g, b = img[h, w, :3]
            lin_r, lin_g, lin_b = lin(r), lin(g), lin(b)

            L = 0.2126 * lin_r + 0.7152 * lin_g + 0.0722 * lin_b
            Lp = L**0.9

            mix = (1.0 - Lp) * Cs + Lp * Ch
            rgb = gam(mix)

            rgb = np.clip(rgb, 0, 255).astype(np.uint8)
            out[h, w, :3] = rgb

            # preserve alpha channel if present (leave untouched)
            if has_alpha:
                out[h, w, 3] = orig[h, w, 3]

    return Image.fromarray(out)


def duotone(filename):
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

    def process_image_to_duotone(filename):
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        processed_filename = f"duotone_{filename}"

        with Image.open(input_path) as img:
            processed_path = os.path.join(UPLOAD_FOLDER, processed_filename)
            duotone_img = do_duotone(img)
            duotone_img.save(processed_path)

        # use the blueprint's uploaded_file endpoint for both original and processed
        original_url = url_for('duotone.uploaded_file', filename=filename)
        processed_url = url_for('duotone.uploaded_file', filename=processed_filename)

        return processed_url, original_url, processed_filename

    return process_image_to_duotone(filename)