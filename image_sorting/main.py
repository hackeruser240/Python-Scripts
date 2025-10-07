import os
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import argparse

# === CONFIGURATION ===
#SOURCE_DIR = r"E:\Images\WhatsApp dumps\2025 - Copy\Sent"
SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png')

# === MODULE: Extract EXIF Creation Date ===
def get_exif_creation_date(filepath):
    try:
        img = Image.open(filepath)
        exif_data = img._getexif()
        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == 'DateTimeOriginal':
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass
    return None

# === MODULE: Fallback to Filesystem Timestamp ===
def get_fallback_creation_date(filepath):
    try:
        return datetime.fromtimestamp(os.path.getmtime(filepath))  # Modified time
    except Exception:
        return None

# === MODULE: Determine Final Creation Date ===
def get_image_creation_date(filepath):
    date = get_exif_creation_date(filepath)
    if not date:
        date = get_fallback_creation_date(filepath)
    return date

# === MODULE: Build Destination Path ===
def build_destination_path(base_dir, date_obj):
    year_folder = os.path.join(base_dir, str(date_obj.year))
    date_folder = os.path.join(year_folder, date_obj.strftime("%d-%b-%Y"))
    os.makedirs(date_folder, exist_ok=True)
    return date_folder

# === MODULE: Move and Delete Image ===
def copy_and_move_to_raw(src_path, dest_folder):
    # Copy to metadata-based folder
    os.makedirs(dest_folder, exist_ok=True)
    copied_path = os.path.join(dest_folder, os.path.basename(src_path))
    shutil.copy2(src_path, copied_path)

    # Move original to Raw subfolder
    raw_folder = os.path.join(os.path.dirname(src_path), "Raw")
    os.makedirs(raw_folder, exist_ok=True)
    moved_path = os.path.join(raw_folder, os.path.basename(src_path))
    shutil.move(src_path, moved_path)

    print(f"Copied → {copied_path}")
    print(f"Moved to Raw → {moved_path}")

# === MAIN BLOCK ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sort images by creation date.")
    parser.add_argument('--source', type=str, required=True,help='Source directory of images')
    args = parser.parse_args()

    SOURCE_DIR = args.source
    SENT_SOURCE_DIR = os.path.join(SOURCE_DIR, "Sent")
    if SENT_SOURCE_DIR:
        DIR=[SOURCE_DIR,SENT_SOURCE_DIR]

    for directory in DIR:
        for filename in os.listdir(directory):
            if not filename.lower().endswith(SUPPORTED_EXTENSIONS):
                continue

            full_path = os.path.join(directory, filename)
            creation_date = get_image_creation_date(full_path)

            if creation_date:
                destination_folder = build_destination_path(directory, creation_date)
                copy_and_move_to_raw(full_path, destination_folder)
            else:
                print(f"Skipped (no date found): {filename}")