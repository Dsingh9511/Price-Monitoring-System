import requests
from bs4 import BeautifulSoup
url = "https://books.toscrape.com/catalogue/dune-dune-1_151/index.html"
page = requests.get("https://books.toscrape.com/catalogue/dune-dune-1_151/index.html")
print(page.status_code)