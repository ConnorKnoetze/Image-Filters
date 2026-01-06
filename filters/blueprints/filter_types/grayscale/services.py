from PIL import Image
import os
import numpy as np
from flask import url_for

def do_grayscale(image, intensity=1):
    width, height = image.size
    array = np.array(image)

    for w in range(width):
        for h in range(height):
            r, g, b = array[h, w][:3]
            gray = (sum([int(r), int(g), int(b)]) // 3) // max(1, (intensity // 4))
            array[h, w] = [gray, gray, gray] + list(array[h, w][3:])  # Preserve alpha if exists

    new_image = Image.fromarray(array)
    return new_image


def grayscale(filename, intensity=1):
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

    def process_image_to_grayscale(filename):
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        processed_filename = f"grayscale_{filename}"

        with Image.open(input_path) as img:
            processed_path = os.path.join(UPLOAD_FOLDER, processed_filename)
            grayscale_img = do_grayscale(img, intensity)
            grayscale_img.save(processed_path)

        # use the blueprint's uploaded_file endpoint for both original and processed
        original_url = url_for('grayscale.uploaded_file', filename=filename)
        processed_url = url_for('grayscale.uploaded_file', filename=processed_filename)

        return processed_url, original_url, processed_filename

    return process_image_to_grayscale(filename)