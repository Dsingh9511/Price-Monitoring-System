import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

def scrape_book(url):
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

    # product_description = soup.find("div", id="product_description").find_next("p").get_text(strip=True)
    # print(product_description) kept crashing due to books with no description (alice in wonderland) upon running a test
    description_tag = soup.find("div", id="product_description")
    if description_tag:
        product_description = description_tag.find_next("p").get_text(strip=True) 
    else:
        product_description = ""
    print(product_description)

    breadcrumb = soup.find_all("a")
    category = breadcrumb[3].get_text(strip=True)
    print(category)

    rating_tag = soup.find("p", class_="star-rating")
    review_rating = rating_tag["class"][1]
    print(review_rating)

    image_src = soup.find("img")["src"]
    image_url = urljoin(url , image_src)
    print(image_url)

    book_data = [product_page_url, universal_product_code, book_title, price_including_tax, price_excluding_tax, quantity_available, product_description, category, review_rating, image_url]
    return book_data

url = "https://books.toscrape.com/catalogue/dune-dune-1_151/index.html"
book = scrape_book(url)

headers = ["product_page_url", "universal_product_code", "book_title", "price_including_tax", "price_excluding_tax", "quantity_available", "product_description", "category", "review_rating", "image_url"]
with open("book.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerow(book)

def get_book_urls(category_url):
    book_urls = []
    page_url = category_url
    while page_url:
        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for article in soup.find_all("article", class_="product_pod"):
            href = article.find("h3").find("a")["href"]
            book_urls.append(urljoin(page_url, href))
        next_button = soup.find("li", class_="next")
        if next_button:
            page_url = urljoin(page_url, next_button.find("a")["href"])
        else:
            page_url = None
    return book_urls

urls = get_book_urls("https://books.toscrape.com/catalogue/category/books/food-and-drink_33/index.html")
print(len(urls))
print(urls[0])

with open("food_and_drink.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    for url in urls:
        book = scrape_book(url)
        writer.writerow(book)

def get_category_urls(home_url):
    category_urls = []
    page = requests.get(home_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for link in soup.select("div.side_categories ul li ul li a"):
        href = link["href"]
        category_urls.append(urljoin(home_url, href))
    return category_urls

categories = get_category_urls("https://books.toscrape.com/")
print(len(categories))
print(categories[0])

for category_url in categories:
    urls = get_book_urls(category_url)
    name = category_url.split("/")[-2]
    with open(f"{name}.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for url in urls:
            writer.writerow(scrape_book(url))