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
print(table_data)
universal_product_code = table_data[0].get_text(strip=True)
print(universal_product_code)