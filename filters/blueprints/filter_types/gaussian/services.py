from PIL import Image
import os
import numpy as np
from flask import url_for
from scipy.ndimage import convolve


def gaussian_kernel(radius, sigma=None):
    if sigma is None:
        sigma = radius/2.0

    ax = np.arange(-radius, radius + 1)
    xx, yy = np.meshgrid(ax, ax)

    kernel = np.exp(-(xx**2 + yy**2) / (2.0 * sigma**2))
    kernel = kernel / np.sum(kernel)

    return kernel


def do_gaussian(image, radius=20):
    arr = np.array(image).astype(np.float64)
    if arr.ndim == 2:
        arr = arr[..., None]

    kernel = gaussian_kernel(radius)
    output = np.zeros_like(arr)

    for c in range(arr.shape[2]):
        output[:, :, c] = convolve(arr[:, :, c], kernel, mode="constant")

    output = np.clip(output, 0, 255).astype(np.uint8)
    if output.shape[2] == 1:
        output = output[:, :, 0]

    return Image.fromarray(output)


def gaussian(filename, radius=20):
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

    def process_image_to_gaussian(filename):
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        processed_filename = f"gaussian_{filename}"

        with Image.open(input_path) as img:
            processed_path = os.path.join(UPLOAD_FOLDER, processed_filename)
            gaussian_img = do_gaussian(img, radius)
            gaussian_img.save(processed_path)

        # use the blueprint's uploaded_file endpoint for both original and processed
        original_url = url_for('gaussian.uploaded_file', filename=filename)
        processed_url = url_for('gaussian.uploaded_file', filename=processed_filename)

        return processed_url, original_url, processed_filename

    return process_image_to_gaussian(filename)