# main.py
import os
from scripts import vids, pics


def create_data_folder(base="Data"):
    if not os.path.exists(base):
        os.makedirs(base)
    return base


def load_links_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def main():
    # === CONFIGURATION ===
    username = "afaqahmad240"
    input_file = "links.txt"

    # === SETUP ===
    data_folder = create_data_folder()
    loader = pics.load_instagram_session(username)

    # === LOAD LINKS ===
    all_links = load_links_from_file(input_file)
    image_posts = []
    video_links = []

    for url in all_links:
        shortcode = pics.extract_shortcode(url)
        post = pics.fetch_post(loader, shortcode)
        if not post:
            continue
        if post.typename in ("GraphSidecar", "GraphImage"):
            image_posts.append((url, post))
        elif post.typename == "GraphVideo":
            video_links.append(url)

    # === PROCESS IMAGES ===
    pics.process_image_posts(image_posts, data_folder)

    # === PROCESS VIDEOS ===
    stats = vids.process_video_links(video_links, data_folder)

    # === SUMMARY ===
    print("\n==== Video Download Summary ====")
    for k, v in stats.items():
        print(f"{k.capitalize()}: {v}")


if __name__ == "__main__":
    main()