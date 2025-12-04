from PIL import Image
import os
import numpy as np
from flask import url_for

def do_inverted(image):
    width, height = image.size
    array = np.array(image)

    for w in range(width):
        for h in range(height):
            r, g, b = array[h, w][:3]
            r = 255 - int(r)
            g = 255 - int(g)
            b = 255 - int(b)
            array[h, w] = [r, g, b] + list(array[h, w][3:])  # Preserve alpha if exists

    new_image = Image.fromarray(array)
    return new_image


def inverted(filename):
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

    def process_image_to_inverted(filename):
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        processed_filename = f"inverted_{filename}"

        with Image.open(input_path) as img:
            processed_path = os.path.join(UPLOAD_FOLDER, processed_filename)
            inverted_img = do_inverted(img)
            inverted_img.save(processed_path)

        # use the blueprint's uploaded_file endpoint for both original and processed
        original_url = url_for('inverted.uploaded_file', filename=filename)
        processed_url = url_for('inverted.uploaded_file', filename=processed_filename)

        return processed_url, original_url, processed_filename

    return process_image_to_inverted(filename)