import requests
from bs4 import BeautifulSoup

HOST = "http://127.0.0.1:12345"

def fetch_page(path):
    url = f"{HOST}{path}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_product_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    product_details = {}
    product_details["name"] = soup.find('h1').text
    product_details["price"] = float(soup.find('h2').text)
    paragraphs = soup.find_all('p')
    product_details["description"] = paragraphs[0].text
    product_details["author"] = paragraphs[1].text
    return product_details

home_content = fetch_page('/')
print("Home Page Content:")
print(home_content)

about_content = fetch_page('/about')
print("About Page Content:")
print(about_content)

faq_content = fetch_page('/faq')
print("FAQ Page Content:")
print(faq_content)

product_listing_content = fetch_page('/product')
soup = BeautifulSoup(product_listing_content, 'html.parser')
product_links = [a['href'] for a in soup.find_all('a', href=True)]
print("Product Page:")
print(product_listing_content)

for product_link in product_links:
    product_content = fetch_page(product_link)
    print("Product Details:")
    print(parse_product_page(product_content))