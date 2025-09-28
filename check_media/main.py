import os
import shutil
from PIL import Image
import cv2

SOURCE_DIR = r"D:\Camera Photos\Recovered Images"
IMAGE_DEST = os.path.join(SOURCE_DIR, "Correct_images")
VIDEO_DEST = os.path.join(SOURCE_DIR, "Correct_videos")

def ensure_directories():
    """Create destination folders if they don't exist."""
    os.makedirs(IMAGE_DEST, exist_ok=True)
    os.makedirs(VIDEO_DEST, exist_ok=True)

def is_image_ok(path):
    """Check if an image file is valid."""
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except Exception:
        return False

def is_video_ok(path):
    """Check if a video file is valid."""
    try:
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            return False
        ret, _ = cap.read()
        cap.release()
        return ret
    except Exception:
        return False

def move_file(src_path, dest_folder):
    """Move a file to the destination folder."""
    try:
        shutil.move(src_path, os.path.join(dest_folder, os.path.basename(src_path)))
    except Exception as e:
        print(f"Failed to move {src_path}: {e}")

def scan_and_validate(directory):
    """Scan directory and validate media files."""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if not os.path.isfile(file_path):
            continue

        ext = os.path.splitext(filename)[1].lower()
        if ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"]:
            if is_image_ok(file_path):
                move_file(file_path, IMAGE_DEST)
        elif ext in [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv"]:
            if is_video_ok(file_path):
                move_file(file_path, VIDEO_DEST)

if __name__ == "__main__":
    ensure_directories()
    scan_and_validate(SOURCE_DIR)
    print("✅ Scan complete. Valid media files have been moved.")