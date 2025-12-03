from flask import request, jsonify, Blueprint, redirect
import os
from werkzeug.utils import secure_filename
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

upload_bp = Blueprint("upload", __name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def _append_query(url, params):
    """Append or replace query parameters on a URL (works for paths like '/filters/pixelate')."""
    parsed = urlparse(url)
    q = dict(parse_qsl(parsed.query))
    q.update(params)
    new_query = urlencode(q)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))

@upload_bp.route('/upload/delete', methods=['POST'])
def delete_upload():
    """
    Expects JSON body: { "filenames": ["original.jpg", "pixelated_original.jpg", ...] }
    Deletes files using secure_filename and returns list of deleted files.
    """
    data = request.get_json(silent=True) or {}
    filenames = data.get('filenames') or []
    deleted = []
    for fn in filenames:
        safe = secure_filename(fn)
        if not allowed_file(safe) and not safe.startswith('pixelated_'):
            if '.' not in safe:
                continue
        path = os.path.join(UPLOAD_FOLDER, safe)
        try:
            if os.path.exists(path):
                os.remove(path)
                deleted.append(safe)
        except Exception:
            pass
    return jsonify({'deleted': deleted}), 200