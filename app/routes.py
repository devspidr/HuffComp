from flask import render_template, request, send_file
import os
from .compression.huffman_core import compressPdfFile, decompressPdfFile

def setup_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == "POST":
            # COMPRESSION ROUTE
            if 'pdf_file_compress' in request.files:
                file = request.files['pdf_file_compress']
                if file.filename.endswith('.pdf'):
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                    file.save(file_path)
                    _, output_path = compressPdfFile(file_path, app.config['COMPRESSED_FOLDER'])
                    return send_file(output_path, as_attachment=True, download_name="compressed_file.huff")

            # DECOMPRESSION ROUTE
            elif 'pdf_file_decompress' in request.files:
                file = request.files['pdf_file_decompress']
                if file.filename.endswith('.huff'):
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                    file.save(file_path)
                    output_pdf_path = decompressPdfFile(file_path, app.config['DECOMPRESSED_FOLDER'])
                    return send_file(output_pdf_path, as_attachment=True, download_name="decompressed_file.pdf")

        return render_template("index.html")
