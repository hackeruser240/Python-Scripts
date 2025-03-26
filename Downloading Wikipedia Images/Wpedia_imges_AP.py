import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import argparse as ag

# Argument parser for aircraft name
parser = ag.ArgumentParser(description="Extracts images and captions from a Wikipedia aircraft page.")
parser.add_argument("--aircraft", required=True, help="Enter name of the aircraft (e.g., Tupolev_Tu-95)")
args = parser.parse_args()

# Wikipedia URL
url = f"https://en.wikipedia.org/wiki/{args.aircraft}"

# Directory setup
base_path = r"C:\Users\HP\Desktop\Py_scripts\Downloading Wikipedia Images"  # Windows path (use raw string)
aircraft_name = args.aircraft
fullpath = os.path.join(base_path, aircraft_name)
if '/' in fullpath:
    fullpath=fullpath.replace("/","-")
    os.makedirs(fullpath, exist_ok=True)  # Create folder if it doesn't exist
else:
    os.makedirs(fullpath, exist_ok=True)  # Create folder if it doesn't exist

# Headers to mimic a browser visit
headers = {"User-Agent": "Mozilla/5.0"}

# Fetch the page content
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Caption file path
caption_file_path = os.path.join(fullpath, "captions.txt")

# Function to download and save an image
def save_image(img_url, filename):
    """Downloads and saves an image from a given URL."""
    try:
        img_data = requests.get(img_url, headers=headers).content
        img_path = os.path.join(fullpath, filename)
        with open(img_path, "wb") as img_file:
            img_file.write(img_data)
        #print(f"Image saved: {img_path}")
    except Exception as e:
        print(f"Failed to save {filename}: {e}")

# Open the caption file once
with open(caption_file_path, "w", encoding="utf-8") as caption_file:
    
    # **Step 1: Extract & Save the Main Image (If Exists)**
    main_caption_div = soup.find("div", class_="ib-aircraft-caption")
    if main_caption_div:
        main_figure = main_caption_div.find_previous("span", typeof="mw:File")
        if main_figure:
            img = main_figure.find("img")
            if img and "src" in img.attrs:
                img_url = urljoin("https:", img["src"])
                save_image(img_url, "0 (Main).jpg")

                # Extract & save caption
                caption_text = main_caption_div.get_text(strip=True) if main_caption_div else "No caption available"
                caption_file.write(f"0 (Main): {caption_text}\n")
                #print(f"Caption saved: {caption_text}")

    # **Step 2: Extract & Save All Other Images**
    figures = soup.find_all("figure", class_="mw-default-size")
    
    for count, figure in enumerate(figures, start=1):
        img = figure.find("img")  # Find image
        if img and "src" in img.attrs:
            img_url = urljoin("https:", img["src"])
            save_image(img_url, f"{count}.jpg")  # Save with numeric name

            # Extract caption text if available
            caption = figure.find("figcaption")
            caption_text = caption.get_text(strip=True) if caption else "No caption available"
            caption_file.write(f"{count}: {caption_text}\n")
    
print("Download complete! Images and captions saved.")