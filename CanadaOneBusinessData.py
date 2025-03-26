import requests
from bs4 import BeautifulSoup

# URL of the CanadaOne business directory (example URL, modify as needed)
url = "https://www.canadaone.com/business/index.html/CanadaOne/directory/map/p/1"

# Send an HTTP request to the page
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

# Check if the request was successful
name=[]
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all business listings (Modify selectors as per actual HTML structure)
    businesses = soup.find_all("li", class_="list-group-item")

    for biz in businesses:
        biz_name = biz.find("a").text.strip() if biz.find("a") else "N/A"
        #address = biz.find("p", class_="address").text.strip() if biz.find("p", class_="address") else "N/A"
        #phone = biz.find("p", class_="phone").text.strip() if biz.find("p", class_="phone") else "N/A"
        #website = biz.find("a", href=True)["href"] if biz.find("a", href=True) else "N/A"

        
        '''
        print(f"Business Name: {name}")
        print(f"Address: {address}")
        print(f"Phone: {phone}")
        print(f"Website: {website}")
        print("-" * 50)
        '''
        
        name.append(biz_name)

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
