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

@upload_bp.route('/upload', methods=['POST'])
def upload_image():
    """
    Saves uploaded file and redirects to the `next` URL with ?filename=<saved-file>
    If no next provided, returns a JSON response with the filename (and pixel_size if present).
    """
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'no file provided'}), 400

    filename = secure_filename(file.filename or '')
    if not filename or not allowed_file(filename):
        return jsonify({'error': 'invalid file type'}), 400

    save_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        file.save(save_path)
    except Exception as e:
        return jsonify({'error': 'failed to save file', 'detail': str(e)}), 500

    pixel_size = (request.form.get('pixel_size') or request.args.get('pixel_size') or '').strip()

    next_url = request.form.get('next') or request.args.get('next')
    if next_url:
        params = {'filename': filename}
        if pixel_size != '':
            params['pixel_size'] = pixel_size
        redirect_url = _append_query(next_url, params)
        return redirect(redirect_url)

    # Fallback: return JSON with uploaded filename and optional pixel_size
    resp = {'filename': filename}
    if pixel_size != '':
        resp['pixel_size'] = pixel_size
    return jsonify(resp), 200

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