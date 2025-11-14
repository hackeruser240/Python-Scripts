import os
import requests
import instaloader

L = instaloader.Instaloader(download_videos=False, save_metadata=False, post_metadata_txt_pattern='')
L.load_session_from_file('afaqahmad240')

shortcode = 'https://www.instagram.com/p/DQjoDO1gOuh/'.split('/')[-2]
folder_name = "1"
os.makedirs(folder_name, exist_ok=True)

try:
    post = instaloader.Post.from_shortcode(L.context, shortcode)
except instaloader.exceptions.BadResponseException:
    print("❌ Failed to fetch post metadata. Check if the shortcode is valid and accessible.")
    exit(1)

for i, node in enumerate(post.get_sidecar_nodes(), start=1):
    url = node.display_url
    response = requests.get(url)
    with open(os.path.join(folder_name, f"{i}.jpg"), "wb") as f:
        f.write(response.content)

print(f"Downloaded {i} images to folder '{folder_name}'")