import subprocess
import os

# Set your file path and output folder
input_file = r"C:\Users\HP\Downloads\yt_links.txt"  # Replace with your file name
output_folder = r"C:\Users\HP\Downloads\yt_shorts"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

with open(input_file, "r") as file:
    links = [line.strip() for line in file if line.strip()]

for link in links:
    try:
        print("********************************")
        print(f"Downloading: {link}")
        subprocess.run(["yt-dlp", "-P", output_folder, link], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to download {link}: {e}")