import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

url = "https://www.amazon.in/s?k=laptops"

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, "html.parser")

products = soup.find_all("div", {"data-component-type": "s-search-result"})

data = []

for product in products:

    # ================= TITLE =================
    title = "N/A"
    title_tag = product.find("span", class_="a-size-medium")
    if title_tag:
        title = title_tag.text.strip()

    # ================= PRICE =================
    price = "N/A"
    price_tag = product.find("span", class_="a-price-whole")
    if price_tag:
        price = price_tag.text.strip()

    # ================= RATING =================
    rating = "N/A"
    rating_tag = product.find("span", class_="a-icon-alt")
    if rating_tag:
        rating = rating_tag.text.strip()

    # ================= IMAGE =================
    image = "N/A"
    image_tag = product.find("img", class_="s-image")
    if image_tag:
        image = image_tag.get("src")

    # ================= AD / ORGANIC =================
    result_type = "Organic"

    sponsored = product.find("span", string="Sponsored")

    if sponsored:
        result_type = "Ad"

    data.append({
        "Title": title,
        "Price": price,
        "Rating": rating,
        "Image": image,
        "Result Type": result_type
    })

    time.sleep(1)

# ================= CREATE DATAFRAME =================
df = pd.DataFrame(data)

# ================= SAVE CSV WITH TIMESTAMP =================
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

filename = f"amazon_laptops_{timestamp}.csv"

df.to_csv(filename, index=False)

print("CSV File Saved Successfully")
print(df.head())
