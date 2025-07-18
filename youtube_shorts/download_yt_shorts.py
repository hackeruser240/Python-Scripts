"""
This script reads a list of YouTube links from 'yt_links.txt' located in the Downloads folder,
and downloads each video using 'yt-dlp' into a specified output directory ('yt_shorts').
If a video has already been downloaded (identified by video ID in filenames), it is skipped.
A summary is printed at the end showing total links, successful downloads, skipped, and failed videos.
"""

import subprocess
import os
from urllib.parse import urlparse, parse_qs


def ensure_output_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_video_id(link):
    parsed = urlparse(link)
    if "youtube.com" in parsed.netloc:
        if parsed.path.startswith("/shorts/"):
            return parsed.path.split("/")[2]
        elif parsed.path.startswith("/watch"):
            return parse_qs(parsed.query).get("v", [None])[0]
    return None


def is_already_downloaded(video_id, folder):
    for fname in os.listdir(folder):
        if video_id and video_id in fname:
            return True
    return False


def load_links(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file if line.strip()]


def download_video(link, output_folder):
    try:
        print("********************************")
        print(f"Downloading: {link}")
        subprocess.run(["yt-dlp", "-P", output_folder, link], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    input_file = r"C:\Users\HP\Downloads\yt_links.txt"
    output_folder = r"C:\Users\HP\Downloads\yt_shorts"

    ensure_output_folder(output_folder)
    links = load_links(input_file)

    total_links = len(links)
    already_downloaded = 0
    unavailable = 0
    downloaded_now = 0

    for link in links:
        video_id = get_video_id(link)
        if is_already_downloaded(video_id, output_folder):
            print(f"Skipping (already downloaded): {link}")
            already_downloaded += 1
            continue
        success = download_video(link, output_folder)
        if success:
            downloaded_now += 1
        else:
            print(f"Unavailable or failed to download: {link}")
            unavailable += 1

    print("\n==== Download Summary ====")
    print(f"Total videos: {total_links}")
    print(f"Total downloaded videos: {downloaded_now}")
    print(f"Unavailable videos: {unavailable}")
    print(f"Already downloaded videos: {already_downloaded}")


if __name__ == "__main__":
    main()