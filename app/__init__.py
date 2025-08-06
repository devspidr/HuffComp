import os
from flask import Flask
from .routes import setup_routes

def create_app():
    app = Flask(__name__)
    root_path = os.path.dirname(os.path.abspath(__file__))  # path to /app

    # Step one directory back to reach HuffCode/
    project_root = os.path.abspath(os.path.join(root_path, os.pardir))

    # Absolute paths for folders
    app.config['UPLOAD_FOLDER'] = os.path.join(project_root, 'uploads')
    app.config['COMPRESSED_FOLDER'] = os.path.join(project_root, 'compressed')
    app.config['DECOMPRESSED_FOLDER'] = os.path.join(project_root, 'decompressed')

    setup_routes(app)
    return app
