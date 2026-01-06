from flask import render_template, Blueprint, request, url_for, send_from_directory
import os
from filters.blueprints.services import get_nav_items

duotone_bp = Blueprint("duotone", __name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@duotone_bp.route('/filters/duotone', methods=['GET'])
def duotone():
    from filters.blueprints.filter_types.duotone.services import duotone
    filename = request.args.get("filename")

    original_url = None
    processed_url = None
    processed_filename = None
    if filename:
        processed_url, original_url, processed_filename = duotone(filename)

    nav_items = get_nav_items("Inverted")

    return render_template(
        "pages/filter_types/duotone/duotone.html",
        original_url=original_url,
        processed_url=processed_url,
        uploaded_filename=filename,
        processed_filename=processed_filename,
        action=url_for('duotone.duotone_upload'),
        next=url_for('duotone.duotone'),
        submit_text='Convert to Inverted',
        nav_items=nav_items
    )

from flask import request, redirect, url_for, jsonify
from filters.blueprints.upload.utils import save_uploaded_file

@duotone_bp.route('/filters/duotone/upload', methods=['POST'])
def duotone_upload():
    """
    Per-filter upload endpoint for duotone:
    - saves file using shared helper
    - redirects to the duotone page with filename
    """
    file = request.files.get('file')
    filename, err = save_uploaded_file(file)
    if err:
        return jsonify({'error': err}), 400
    params = {'filename': filename}
    return redirect(url_for('duotone.duotone', **params))

@duotone_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)