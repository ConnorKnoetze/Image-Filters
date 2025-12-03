import os

from PIL import Image
from flask import url_for
from werkzeug.utils import secure_filename

from filters.blueprints.filter_types.pixelate.pixelate import allowed_file
from filters.blueprints.upload.upload import UPLOAD_FOLDER


def pixelate(filename):
    filename = secure_filename(filename)
    original_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(original_path) and allowed_file(filename):
        try:
            img = Image.open(original_path)
            w, h = img.size
            pixel_size = 16
            small_w = max(1, w // pixel_size)
            small_h = max(1, h // pixel_size)
            img_small = img.resize((small_w, small_h), resample=Image.NEAREST)
            img_pixelated = img_small.resize((w, h), Image.NEAREST)

            processed_filename = f"pixelated_{filename}"
            processed_path = os.path.join(UPLOAD_FOLDER, processed_filename)
            img_pixelated.save(processed_path)

            original_url = url_for("pixelate.uploaded_file", filename=filename)
            processed_url = url_for(
                "pixelate.uploaded_file", filename=processed_filename
            )
            return processed_url, original_url, processed_filename
        except Exception:
            original_url = None
            processed_url = None
            return processed_url, original_url, None
    return None, None, None