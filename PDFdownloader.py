import requests
from bs4 import BeautifulSoup
import os
import argparse

parser=argparse.ArgumentParser()

parser.add_argument('--link',type=str,required=True,help='Mention your website link from where you want to download the PDFs')
parser.add_argument('--folder_name',type=str,required=True,help='Mention the path where you want to save the PDFs')
args=parser.parse_args()


# URL of the webpage containing the PDF links
#url = "https://math.berkeley.edu/~ehallman/fall-2015/"
url=args.link

# Send a GET request to the webpage
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all the links on the webpage
links = soup.find_all("a")

#Set the pdf variable:
folder_pdf_name=args.folder_name    

# Create a directory to save the PDFs (if it doesn't exist)
if not os.path.exists(folder_pdf_name):
    os.makedirs(folder_pdf_name)

# Iterate through the links and download PDFs
for link in links:
    href = link.get("href")
    if href==None:
        continue
        
    if href.endswith(".ppt"):
        pdf_url = url + href 
        pdf_name = pdf_url.split("/")[-1]
        pdf_path = os.path.join(folder_pdf_name, pdf_name)
        # Download the PDF file
        with open(pdf_path, "wb") as f:
            pdf_response = requests.get(pdf_url)
            f.write(pdf_response.content)
            print(f"Downloaded: {pdf_name}")