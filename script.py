import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

BASE_URL = "https://qbdadvisor.com/shop/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
max_products = 18
def extract_products(url, max_products=max_products):
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    products = []

    for link in soup.find_all("a", href=True):
        href = urljoin(BASE_URL, link["href"])
        if "/product/" in href.lower():
            title = link.get("title") or link.text.strip()
            if title and href not in [p['url'] for p in products]:
                products.append({"title": title, "url": href})
                if len(products) >= max_products:
                    break

    return products

def extract_product_details(product_url):
    res = requests.get(product_url, headers=HEADERS)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    title = soup.find("h1").text.strip() if soup.find("h1") else ""
    price_tag = soup.select_one(".price, .woocommerce-Price-amount")
    price = price_tag.text.strip() if price_tag else ""

    # Extract the main description from wd-single-content
    desc_div = soup.find("div", class_="elementor-widget-woocommerce-product-content")
    description = desc_div.get_text(separator="\n", strip=True) if desc_div else ""

    sku_span = soup.find("span", class_="sku")
    sku = sku_span.get_text(separator="\n", strip=True) if desc_div else ""

    return {
        "title": title,
        "price": price,
        "description": description,
        "sku": sku,
        "url": product_url
    }

if __name__ == "__main__":
    print(f"[*] Scraping up to {max_products} products...")
    product_list = extract_products(BASE_URL, max_products=max_products)

    for i, product in enumerate(product_list):
        print(f"\n--- Product {i+1} ---")
        details = extract_product_details(product["url"])
        print(f"Title: {details['title']}")
        print(f"Price: {details['price']}")
        print(f"URL: {details['url']}")
        print(f"Sku: {details['sku']}")
        print(f"Description (preview):\n{details['description']}...")
        time.sleep(1)  # polite delay