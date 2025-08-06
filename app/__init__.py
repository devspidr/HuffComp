import os
from flask import Flask
from .routes import setup_routes

def create_app():
    root_path = os.path.dirname(os.path.abspath(__file__))  # path to /app

    # Step one directory back to reach HuffCode/
    project_root = os.path.abspath(os.path.join(root_path, os.pardir))

    app = Flask(
    __name__,
    template_folder=os.path.join(root_path, 'templates'),  # this is app/templates
    static_folder=os.path.join(root_path, 'static')        # this is app/static
)


    # Folder config for file operations
    app.config['UPLOAD_FOLDER'] = os.path.join(project_root, 'uploads')
    app.config['COMPRESSED_FOLDER'] = os.path.join(project_root, 'compressed')
    app.config['DECOMPRESSED_FOLDER'] = os.path.join(project_root, 'decompressed')

    setup_routes(app)
    return app
