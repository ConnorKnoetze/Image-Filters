from flask import render_template, Blueprint, request, url_for, send_from_directory
import os
from filters.blueprints.services import get_nav_items

pixelate_bp = Blueprint("pixelate", __name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@pixelate_bp.route('/filters/pixelate', methods=['GET'])
def pixelate():
    from filters.blueprints.filter_types.pixelate.services import pixelate
    filename = request.args.get("filename")

    raw_pixel = request.args.get("pixel_size") or request.form.get("pixel_size") or None
    try:
        pixel_size = int(raw_pixel) if raw_pixel not in (None, "") else None
    except ValueError:
        pixel_size = None

    original_url = None
    processed_url = None
    processed_filename = None
    if filename:
        processed_url, original_url, processed_filename = pixelate(filename, pixel_size=pixel_size)

    nav_items = get_nav_items("Pixelate")

    return render_template(
        "pages/filter_types/pixelate/pixelate.html",
        original_url=original_url,
        processed_url=processed_url,
        uploaded_filename=filename,
        processed_filename=processed_filename,
        action=url_for('upload.upload_image'),
        next=url_for('pixelate.pixelate'),
        submit_text='Pixelate Image',
        nav_items=nav_items
    )

@pixelate_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)