from flask import render_template, Blueprint, request, url_for, send_from_directory
import os
from filters.blueprints.services import get_nav_items

inverted_bp = Blueprint("inverted", __name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@inverted_bp.route('/filters/inverted', methods=['GET'])
def inverted():
    from filters.blueprints.filter_types.inverted.services import inverted
    filename = request.args.get("filename")

    original_url = None
    processed_url = None
    processed_filename = None
    if filename:
        processed_url, original_url, processed_filename = inverted(filename)

    nav_items = get_nav_items("Inverted")

    return render_template(
        "pages/filter_types/inverted/inverted.html",
        original_url=original_url,
        processed_url=processed_url,
        uploaded_filename=filename,
        processed_filename=processed_filename,
        action=url_for('inverted.inverted_upload'),
        next=url_for('inverted.inverted'),
        submit_text='Convert to Inverted',
        nav_items=nav_items
    )

from flask import request, redirect, url_for, jsonify
from filters.blueprints.upload.utils import save_uploaded_file

@inverted_bp.route('/filters/inverted/upload', methods=['POST'])
def inverted_upload():
    """
    Per-filter upload endpoint for inverted:
    - saves file using shared helper
    - redirects to the inverted page with filename
    """
    file = request.files.get('file')
    filename, err = save_uploaded_file(file)
    if err:
        return jsonify({'error': err}), 400
    params = {'filename': filename}
    return redirect(url_for('inverted.inverted', **params))

@inverted_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)