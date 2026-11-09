import requests
from bs4 import BeautifulSoup
url = "https://books.toscrape.com/catalogue/dune-dune-1_151/index.html"
page = requests.get("url")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')
book_title = soup.find("h1").get_text(strip=True)
print(book_title)