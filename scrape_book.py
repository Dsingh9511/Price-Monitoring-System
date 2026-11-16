import requests
from bs4 import BeautifulSoup
url = "https://books.toscrape.com/catalogue/dune-dune-1_151/index.html"
page = requests.get(url)
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')
book_title = soup.find("h1").get_text(strip=True)
print(book_title)
product_page_url = url
print(product_page_url)

table_data = soup.find_all("td")
universal_product_code = table_data[0].get_text(strip=True)
print(universal_product_code)
price_including_tax = table_data[3].get_text(strip=True)
print(price_including_tax)
price_excluding_tax = table_data[2].get_text(strip=True)
print(price_excluding_tax)

availability = table_data[5].get_text(strip=True)
quantity_available = availability
print(quantity_available)

product_description = soup.find("div", id="product_description").find_next("p").get_text(strip=True)
print(product_description)

breadcrumb = soup.find_all("a")
category = breadcrumb[3].get_text(strip=True)
print(category)

rating_tag = soup.find("p", class_="star-rating")
review_rating = rating_tag["class"][1]
print(review_rating)

from urllib.parse import urljoin
image_src = soup.find("img")["src"]
image_url = urljoin(url , image_src)
print(image_url)

import csv
headers = ["product_page_url", "universal_product_code", "book_title", "price_including_tax", "price_excluding_tax", "quantity_available", "product_description", "category", "review_rating", "image_url"]
book_data = [product_page_url, universal_product_code, book_title, price_including_tax, price_excluding_tax, quantity_available, product_description, category, review_rating, image_url]
with open("book.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(headers)    
    writer.writerow(book_data)