import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import argparse as ag

# Boeing Aircraft list:

boeing_military_aircraft = [
    # Bombers
    "Boeing B-17 Flying Fortress",
    "Boeing B-29 Superfortress",
    "Boeing B-47 Stratojet",
    "Boeing B-50 Superfortress",
    "Boeing B-52 Stratofortress",
    
    # Fighter and Attack Aircraft
    "Boeing P-12",
    "Boeing P-26 Peashooter",
    "McDonnell Douglas F-15 Eagle",
    "Boeing F-15EX Eagle II",
    "McDonnell Douglas F/A-18 Hornet", 
    "Boeing F/A-18E/F Super Hornet",
    
    # Transport and Tanker Aircraft
    "Boeing C-17 Globemaster III",
    "Boeing KC-135 Stratotanker",
    "Boeing KC-767",
    "Boeing KC-46 Pegasus",
    
    # Helicopters
    "Boeing AH-64 Apache",
    "Boeing CH-47 Chinook",
    "Boeing Vertol CH-46 Sea Knight",
    
    # Maritime Patrol and Reconnaissance Aircraft
    "Boeing P-8 Poseidon",
    
    # Electronic Warfare and Surveillance Aircraft
    "Boeing E-3 Sentry",
    "Boeing E-4B",
    "Boeing E-6 Mercury",
    "Boeing E-8 Joint STARS",
    
    # Unmanned Aerial Vehicles (UAVs)
    "Boeing MQ-25 Stingray",
    "Boeing Insitu RQ-21 Blackjack",
    
    # Experimental and Prototype Aircraft
    "Boeing X-32",
    "Boeing X-45"
]

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

for item in boeing_military_aircraft:
    print(f"{boeing_military_aircraft.index(item)}: Working on {item}")

    # Wikipedia URL
    url = f"https://en.wikipedia.org/wiki/{item}"

    # Directory setup
    base_path = r"C:\Users\HP\Desktop\Py_scripts\Downloading Wikipedia Images\Boeing Military"  # Windows path (use raw string)
    aircraft_name = item
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