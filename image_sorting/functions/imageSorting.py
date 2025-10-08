import os
import shutil
import argparse
import subprocess
import json
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import exifread
from image_sorting.loggers.LOCAL_loggerSetup import local_loggerSetup

logger=local_loggerSetup("imageSorting.py")
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png')
VIDEO_EXTENSIONS = ('.mp4', '.mkv', '.mov', '.avi', '.m4a', '.webm')
SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS + VIDEO_EXTENSIONS

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

def get_xmp_creation_date(filepath):
    try:
        with open(filepath, 'rb') as f:
            tags = exifread.process_file(f, stop_tag="DateTimeOriginal", details=False)
            for tag in ["EXIF DateTimeOriginal", "EXIF CreateDate"]:
                if tag in tags:
                    return datetime.strptime(str(tags[tag]), "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass
    return None

def get_video_creation_date(filepath):
    try:
        cmd = [
            'ffprobe', '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            filepath
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        metadata = json.loads(result.stdout)
        creation_time = metadata['format']['tags'].get('creation_time')
        if creation_time:
            return datetime.fromisoformat(creation_time.replace('Z', '+00:00'))
    except Exception:
        pass
    return None

def get_filesystem_dates(filepath):
    try:
        stat = os.stat(filepath)
        created = datetime.fromtimestamp(stat.st_ctime)
        modified = datetime.fromtimestamp(stat.st_mtime)
        return [created, modified]
    except Exception:
        return []

def normalize_datetime(dt):
    if dt.tzinfo is not None:
        return dt.astimezone(tz=None).replace(tzinfo=None)
    return dt

def get_file_creation_date(filepath):
    dates = []

    ext = os.path.splitext(filepath)[1].lower()

    if ext in IMAGE_EXTENSIONS:
        exif_date = get_exif_creation_date(filepath)
        if exif_date:
            dates.append(exif_date)

        xmp_date = get_xmp_creation_date(filepath)
        if xmp_date:
            dates.append(xmp_date)

    elif ext in VIDEO_EXTENSIONS:
        video_date = get_video_creation_date(filepath)
        if video_date:
            dates.append(video_date)

    fs_dates = get_filesystem_dates(filepath)
    dates.extend(fs_dates)

    valid_dates = [normalize_datetime(d) for d in dates if d is not None]
    if valid_dates:
        return min(valid_dates)

    logger.info(f"⚠️ Fallback used for: {os.path.basename(filepath)}")
    return None

def build_destination_path(base_dir, date_obj):
    year_folder = os.path.join(base_dir, str(date_obj.year))
    date_folder = os.path.join(year_folder, date_obj.strftime("%d-%b-%Y"))
    os.makedirs(date_folder, exist_ok=True)
    return date_folder

def copy_and_move_to_raw(src_path, dest_folder):
    os.makedirs(dest_folder, exist_ok=True)
    copied_path = os.path.join(dest_folder, os.path.basename(src_path))
    shutil.copy2(src_path, copied_path)

    raw_folder = os.path.join(os.path.dirname(src_path), "Raw")
    os.makedirs(raw_folder, exist_ok=True)
    moved_path = os.path.join(raw_folder, os.path.basename(src_path))
    #shutil.move(src_path, moved_path)

    logger.info(f"Copied → {copied_path}")
    logger.info(f"Moved to Raw → {moved_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sort images and videos by earliest creation date.")
    parser.add_argument('--source', type=str, required=True, help='Source directory of media files')
    args = parser.parse_args()

    logger=local_loggerSetup("imageSorting.py")
    logger.info(f"Script started with source: {args.source}")

    SOURCE_DIR = args.source
    SENT_SOURCE_DIR = os.path.join(SOURCE_DIR, "Sent")
    DIR = [SOURCE_DIR]
    if os.path.exists(SENT_SOURCE_DIR):
        DIR.append(SENT_SOURCE_DIR)

    for directory in DIR:
        for filename in os.listdir(directory):
            if not filename.lower().endswith(SUPPORTED_EXTENSIONS):
                continue

            full_path = os.path.join(directory, filename)
            creation_date = get_file_creation_date(full_path)

            if creation_date:
                destination_folder = build_destination_path(directory, creation_date)
                copy_and_move_to_raw(full_path, destination_folder)
            else:
                logger.info(f"Skipped (no date found): {filename}")