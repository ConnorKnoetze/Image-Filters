from flask import render_template, Blueprint, request, url_for, send_from_directory
import os
from filters.blueprints.services import get_nav_items

gaussian_bp = Blueprint("gaussian", __name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@gaussian_bp.route('/filters/gaussian', methods=['GET'])
def gaussian():
    from filters.blueprints.filter_types.gaussian.services import gaussian
    filename = request.args.get("filename")

    raw_radius = request.args.get("radius") or request.form.get("radius") or None
    try:
        radius = int(raw_radius) if raw_radius not in (None, "") else None
    except ValueError:
        radius = None

    original_url = None
    processed_url = None
    processed_filename = None
    if filename:
        processed_url, original_url, processed_filename = gaussian(filename, radius=radius)

    nav_items = get_nav_items("gaussian")

    return render_template(
        "pages/filter_types/gaussian/gaussian.html",
        original_url=original_url,
        processed_url=processed_url,
        uploaded_filename=filename,
        processed_filename=processed_filename,
        action=url_for('gaussian.gaussian_upload'),
        next=url_for('gaussian.gaussian'),
        submit_text='Convert to gaussian',
        nav_items=nav_items
    )

from flask import request, redirect, url_for, jsonify
from filters.blueprints.upload.utils import save_uploaded_file

@gaussian_bp.route('/filters/gaussian/upload', methods=['POST'])
def gaussian_upload():
    """
    Per-filter upload endpoint for gaussian:
    - saves file using shared helper
    - reads filter-specific value (e.g. `radius`)
    - redirects to the gaussian page with filename and radius
    """
    file = request.files.get('file')
    filename, err = save_uploaded_file(file)
    if err:
        return jsonify({'error': err}), 400

    radius = request.form.get('radius') or request.args.get('radius') or ''
    params = {'filename': filename}
    if radius != '':
        params['radius'] = radius
    return redirect(url_for('gaussian.gaussian', **params))

@gaussian_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)