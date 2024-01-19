import requests
from bs4 import BeautifulSoup
import argparse
import csv

def get_product_list(product_type, max_price):
    base_url = "https://www.gadgetbytenepal.com"
    if product_type == "mobile":
        url = f"{base_url}/category/mobile-price-in-nepal/"
    elif product_type == "laptop":
        url = f"{base_url}/category/laptop-price-in-nepal/"
    else:
        print("Invalid product type. Please choose 'mobile' or 'laptop'.")
        return []

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    products = []
    for product in soup.find_all("div", class_="entry-summary"):
        title = product.find("h2", class_="woocommerce-loop-product__title").text.strip()
        price = product.find("span", class_="woocommerce-Price-amount").text.strip()

        price = int(price.replace(",", ""))
        if price <= max_price:
            products.append((title, price))

    return products

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape GadgetByte Nepal for products and save to CSV.")
    parser.add_argument("--type", help="Product type (mobile or laptop)")
    parser.add_argument("--max-price", type=int, help="Maximum price")
    parser.add_argument("--output", default="output.csv", help="Output CSV file name")
    args = parser.parse_args()

    if args.type and args.max_price:
        products = get_product_list(args.type, args.max_price)

        if products:
            with open(args.output, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Title", "Price"])

                for product in products:
                    writer.writerow([product[0], product[1]])

            print(f"Data saved to {args.output}")
        else:
            print(f"No products found under {args.max_price} NPR for {args.type}.")
    else:
        print("Please provide both product type and maximum price.")
