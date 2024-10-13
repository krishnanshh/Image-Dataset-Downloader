import os
import zipfile
from bing_image_downloader import downloader
import logging

def download_images(keyword, num_images, download_path):
    logging.debug(f"Downloading images for keyword: {keyword} to path: {download_path}")
    downloader.download(keyword, limit=num_images, output_dir=download_path, adult_filter_off=True, force_replace=False, timeout=60)

def create_zip(download_path, zip_path):
    logging.debug(f"Creating zip file: {zip_path} from path: {download_path}")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, _, files in os.walk(download_path):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)
    logging.debug(f"Zip file created: {zip_path}")
