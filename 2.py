# this is the small project that i am just doing to get familiar with playwright. in this project, i am extracting data of e-commerce website.
#step 1: Importing the modules
import json
import logging
from bs4 import PageElement

from flask.cli import load_dotenv

import sys
print(sys.path)

import subprocess
import time
import urllib
from logging import  getLogger
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright


# step 2: setting up logging and reading username & access key
logger = getLogger("webscapper.py")
logging.basicConfig(
    stream=sys.stdout, 
    format="%(asctime)s--%(levelname)s--%(message)s",
    level=logging.DEBUG,
)
# read username and access key from sample.env file
load_dotenv("sample.env")


# open the website
page.goto("https://ecommerce-playground.lambdatest.io/")

# click on "shop by category....
# here, get_by_role() locator to nvaigate & perform click() action
page.get_by_role("button", name="Shop by Category").click()

#click on the software(it is a element that shows the link)
page.get_by_role("link", name="Software").click()

# software page displays 15 products, we want to change it to 75
page_to_be_scrapped = page.get_by_role(
    "Combobox", name="Show:"
).select_option(
    "https://ecommerce-playground.lambdatest.io/index.php?route=product/category&path=17&limit=75"
)
page.goto(page_to_be_scrapped[0])

# process for laoading the images




# preparing the base locator
base_product_row_locator = (
    page.locator("#entry_212408").location(".row").locator(".product-grid")
)


# locating product name, price and images
# product name is conatined within h4
# product price is contained in a div with class = price - new
# image is present in class=carousel-inner active

product_name = base_product_row_locator.get_by_role("heading")
product_price = base_product_row_locator.locator(".price-new")
product_image = (
    base_product_row_locator.location(".carousel-inner")
    .locator(".active")
    .get_by_role("img")
)


# scraping the data 
total_products = base_product_row_locator.count()
for product in range(total_products):
    logger.info(
    f"\n**** PRODUCT {product+1} ****\n"
                    f"Product Name = {product_name.nth(product).all_inner_texts()[0]}\n"
                    f"Price = {product_price.nth(product).all_inner_texts()[0]}\n"
                    f"Image = {product_image.nth(product).get_attribute('src')}\n"
                    
    )