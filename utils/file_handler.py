import os
from werkzeug.utils import secure_filename
from config import Config

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def save_upload(file):
    if not os.path.exists(Config.UPLOAD_FOLDER):
        os.makedirs(Config.UPLOAD_FOLDER)
        
    filename = secure_filename(file.filename)
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(filepath)
    return filepath