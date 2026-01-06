import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    """
    Returns (filename, None) on success or (None, error_message) on failure.
    """
    if not file:
        return None, 'no file provided'
    filename = secure_filename(file.filename or '')
    if not filename or not allowed_file(filename):
        return None, 'invalid file type'
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        file.save(save_path)
        return filename, None
    except Exception as e:
        return None, f'failed to save file: {e}'
