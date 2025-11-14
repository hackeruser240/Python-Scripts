# scripts/vids.py
import subprocess
import os
from urllib.parse import urlparse


def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_video_id(link):
    parsed = urlparse(link)
    if "instagram.com" in parsed.netloc:
        parts = [p for p in parsed.path.split('/') if p]
        return parts[-1] if parts else None
    return None


def is_already_downloaded(video_id, folder):
    if not video_id:
        return False
    return any(video_id in fname for fname in os.listdir(folder))


def download_video(link, output_folder):
    try:
        print(f"🎥 Downloading: {link}")
        subprocess.run(["yt-dlp", "-P", output_folder, link], check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to download: {link}")
        return False


def process_video_links(links, output_folder):
    ensure_folder(output_folder)
    stats = {"total": 0, "downloaded": 0, "skipped": 0, "failed": 0}

    for link in links:
        stats["total"] += 1
        vid_id = get_video_id(link)
        if is_already_downloaded(vid_id, output_folder):
            print(f"⏩ Skipping (already downloaded): {link}")
            stats["skipped"] += 1
            continue
        if download_video(link, output_folder):
            stats["downloaded"] += 1
        else:
            stats["failed"] += 1

    return stats