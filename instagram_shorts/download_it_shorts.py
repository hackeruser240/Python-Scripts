# filename: download_it_videos.py
import subprocess
import os
from urllib.parse import urlparse, parse_qs


def ensure_output_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_video_id(link):
    # This function needs to be adapted for Instagram's URL structure to extract a unique ID
    # For simplicity, we'll use the last part of the path as a pseudo-ID for now.
    parsed = urlparse(link)
    if "instagram.com" in parsed.netloc:
        path_parts = [part for part in parsed.path.split('/') if part]
        if path_parts:
            # This is a basic attempt; a more robust solution might involve API calls or deeper parsing
            return path_parts[-1]
    return None


def is_already_downloaded(video_id, folder):
    if not video_id:
        return False
    for fname in os.listdir(folder):
        if video_id in fname:
            return True
    return False


def load_links(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file if line.strip()]


def download_video(link, output_folder):
    try:
        print("********************************")
        print(f"Downloading: {link}")
        # yt-dlp can handle Instagram links directly
        subprocess.run(["yt-dlp", "-P", output_folder, link], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    input_file = r"C:\Users\HP\Downloads\it_links.txt" # Adjusted file name
    output_folder = r"C:\Users\HP\Downloads\it_videos" # Adjusted folder name

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