# scripts/pics.py
import os
import requests
import instaloader


def load_instagram_session(username: str) -> instaloader.Instaloader:
    loader = instaloader.Instaloader(download_videos=False, save_metadata=False, post_metadata_txt_pattern='')
    loader.load_session_from_file(username)
    return loader


def extract_shortcode(url: str) -> str:
    return url.strip('/').split('/')[-1]


def fetch_post(loader: instaloader.Instaloader, shortcode: str) -> instaloader.Post | None:
    try:
        return instaloader.Post.from_shortcode(loader.context, shortcode)
    except instaloader.exceptions.BadResponseException:
        print(f"❌ Failed to fetch post metadata: {shortcode}")
        return None


def get_next_folder_index(base_path: str) -> str:
    existing = [int(name) for name in os.listdir(base_path) if name.isdigit()]
    return str(max(existing, default=0) + 1)


def download_slider_images(post: instaloader.Post, folder_path: str):
    os.makedirs(folder_path, exist_ok=True)
    count = 0

    if post.typename == "GraphImage":
        url = post.url
        response = requests.get(url)
        with open(os.path.join(folder_path, "1.jpg"), "wb") as f:
            f.write(response.content)
        count = 1

    elif post.typename == "GraphSidecar":
        for count, node in enumerate(post.get_sidecar_nodes(), start=1):
            url = node.display_url
            response = requests.get(url)
            with open(os.path.join(folder_path, f"{count}.jpg"), "wb") as f:
                f.write(response.content)

    if count > 0:
        print(f"✅ Downloaded {count} image(s) to '{folder_path}'")
    else:
        print(f"⚠️ No images found in post. Nothing downloaded to '{folder_path}'")


def process_image_posts(post_tuples, base_folder):
    for url, post in post_tuples:
        folder_name = get_next_folder_index(base_folder)
        folder_path = os.path.join(base_folder, folder_name)
        download_slider_images(post, folder_path)