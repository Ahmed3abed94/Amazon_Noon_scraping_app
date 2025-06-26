from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys
from urllib.parse import quote
from bs4 import BeautifulSoup

def scrap_noon(driver, search_query):
    # Encode the search query so it can be safely included in a URL
    encoded_query = quote(search_query)
    
    # Open the Noon search page for the encoded query
    driver.get(f"https://www.noon.com/egypt-en/search/?q={encoded_query}")

    # Wait until at least one product container is loaded on the page (max wait 1000 seconds)
    WebDriverWait(driver, 1000).until(
         EC.presence_of_element_located((By.CSS_SELECTOR, "div.ProductBoxVertical_wrapper__xPj_f"))
    )
    
    # Get the full HTML content of the loaded page
    html = driver.page_source

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find all product containers using their CSS class
    product_divs = soup.find_all("div", {"class": "ProductBoxVertical_wrapper__xPj_f"})
    
    product_list = []  # List to hold the scraped product info
    
    # Loop through each product container and extract details
    for product in product_divs:
        try:
            # Extract product title from the specified h2 element
            title = product.find("h2", {"class": "ProductDetailsSection_title__JorAV"}).text.strip()
            
            # Extract product price from the strong element with price class
            price = product.find("strong", {"class": "Price_amount__2sXa7"}).text.strip()
            
            # Extract product image URL from the img tag with specific class
            img = product.find("img", {"class": "ProductImageCarousel_productImage__jtsOn"})["src"]
            
            # Append the product data as a dictionary to the list
            product_list.append({
                "title": title,
                "price": price,
                "img": img
            })
        except Exception as e:
            # If any info is missing or parsing fails, print the error and continue
            print(e)
    
    # Return the list of scraped products
    return product_list
