import requests
from bs4 import BeautifulSoup

class PhotoUtils:
    def get_google_image(query: str, image_amount: int):
        query = query.replace(" ", "+")
        url = f"https://www.google.com/search?tbm=isch&q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        img_tags = soup.find_all("img")
        if len(img_tags) > 1:
            image_urls = []

            for img_tag in img_tags:
                image_urls.append(img_tag["src"])
            
            return image_urls
        
        return "No images found."