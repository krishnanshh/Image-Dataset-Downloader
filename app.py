from flask import Flask, request, send_file, jsonify, render_template
import os
import uuid
import logging
from image_downloader import download_images, create_zip

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    keyword = data['keyword']
    num_images = int(data['num_images'])
    session_id = str(uuid.uuid4())
    download_path = os.path.join('downloads', f'{keyword}')
    zip_filename = f'{keyword}.zip'
    zip_path = os.path.abspath(os.path.join('downloads', zip_filename))

    logging.debug(f"Download path: {download_path}")
    logging.debug(f"Zip path: {zip_path}")

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    download_images(keyword, num_images, download_path)
    create_zip(download_path, zip_path)

    if os.path.exists(zip_path):
        logging.debug(f"Zip file created: {zip_path}")
        return jsonify({'zip_path': zip_path, 'zip_filename': zip_filename})
    else:
        logging.error(f"Zip file was not created: {zip_path}")
        return jsonify({'error': 'Zip file was not created.'}), 500

@app.route('/download_zip', methods=['GET'])
def download_zip():
    zip_path = request.args.get('zip_path')
    logging.debug(f"Attempting to send file: {zip_path}")
    if os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True)
    else:
        logging.error(f"File not found: {zip_path}")
        return jsonify({'error': 'File not found.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
