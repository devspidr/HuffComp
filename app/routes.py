from flask import render_template, request, send_file, send_from_directory, current_app
import os
from .compression.huffman_core import compressPdfFile, decompressPdfFile

def setup_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == "POST":
            action = request.form.get('action')

            # 🟢 COMPRESSION
            if action == 'compress' and 'pdf_file' in request.files:
                file = request.files['pdf_file']
                if file.filename.endswith('.pdf') or file.filename.endswith('.txt'):
                    filename = file.filename
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)

                    original_size = os.path.getsize(file_path)
                    _, output_path = compressPdfFile(file_path, app.config['COMPRESSED_FOLDER'])
                    compressed_size = os.path.getsize(output_path)

                    compression_ratio = round(100 * (1 - compressed_size / original_size), 2)
                    original_size_kb = round(original_size / 1024, 2)
                    compressed_size_kb = round(compressed_size / 1024, 2)

                    ineffective_compression = compression_ratio <= 0

                    return render_template(
                        "index.html",
                        compression_ratio=compression_ratio,
                        original_size_kb=original_size_kb,
                        compressed_size_kb=compressed_size_kb,
                        show_download=True,
                        compressed_filename=os.path.basename(output_path),
                        ineffective_compression=ineffective_compression
                    )

            # 🟢 DECOMPRESSION
            elif action == 'decompress' and 'huff_file' in request.files:
                file = request.files['huff_file']
                if file.filename.endswith('.huff'):
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                    file.save(file_path)

                    output_pdf_path = decompressPdfFile(file_path, app.config['DECOMPRESSED_FOLDER'])
                    return send_file(output_pdf_path, as_attachment=True, download_name="decompressed_file.pdf")

        # Default GET or fallback
        return render_template("index.html")

    @app.route('/download/<filename>')
    def download_file(filename):
        return send_from_directory(app.config['COMPRESSED_FOLDER'], filename, as_attachment=True)
