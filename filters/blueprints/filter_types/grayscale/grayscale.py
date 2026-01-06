from flask import render_template, Blueprint, request, url_for, send_from_directory
import os
from filters.blueprints.services import get_nav_items

grayscale_bp = Blueprint("grayscale", __name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@grayscale_bp.route('/filters/grayscale', methods=['GET'])
def grayscale():
    from filters.blueprints.filter_types.grayscale.services import grayscale
    filename = request.args.get("filename")

    raw_intensity = request.args.get("intensity") or request.form.get("intensity") or None
    try:
        intensity = int(raw_intensity) if raw_intensity not in (None, "") else None
    except ValueError:
        intensity = None

    original_url = None
    processed_url = None
    processed_filename = None
    if filename:
        processed_url, original_url, processed_filename = grayscale(filename, intensity=intensity)

    nav_items = get_nav_items("Grayscale")

    return render_template(
        "pages/filter_types/grayscale/grayscale.html",
        original_url=original_url,
        processed_url=processed_url,
        uploaded_filename=filename,
        processed_filename=processed_filename,
        action=url_for('grayscale.grayscale_upload'),
        next=url_for('grayscale.grayscale'),
        submit_text='Convert to Grayscale',
        nav_items=nav_items
    )

from flask import request, redirect, url_for, jsonify
from filters.blueprints.upload.utils import save_uploaded_file

@grayscale_bp.route('/filters/grayscale/upload', methods=['POST'])
def grayscale_upload():
    """
    Per-filter upload endpoint for grayscale:
    - saves file using shared helper
    - reads filter-specific value (e.g. `intensity`)
    - redirects to the grayscale page with filename and intensity
    """
    file = request.files.get('file')
    filename, err = save_uploaded_file(file)
    if err:
        return jsonify({'error': err}), 400

    intensity = request.form.get('intensity') or request.args.get('intensity') or ''
    params = {'filename': filename}
    if intensity != '':
        params['intensity'] = intensity
    return redirect(url_for('grayscale.grayscale', **params))

@grayscale_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)