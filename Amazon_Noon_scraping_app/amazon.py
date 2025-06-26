from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Amazon_Noon_scraping_app.utilis import init_driver
import pandas as pd
import time
from urllib.parse import quote_plus

# Function to scrape products from Amazon based on the search query
def amazone_scrap(driver, search_query):
    # Encode the search query to be URL safe
    qoute = quote_plus(search_query)
    # Navigate to the Amazon Egypt search results page with the query
    driver.get(f"https://www.amazon.eg/s?k={qoute}&ref=nb_sb_noss")

    item_list = []  # List to store scraped product data

    while True:
        # Wait until product titles are present on the page to ensure the page has loaded
        WebDriverWait(driver, 1000).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//a[contains(@class, "a-link-normal") and contains(@href, "/dp/")]/h2/span')
            )
        )
        
        # Find all product title elements
        titles = driver.find_elements(By.XPATH, '//a[contains(@class, "a-link-normal") and contains(@href, "/dp/")]/h2/span')
        # Find all product price elements
        prices = driver.find_elements(By.XPATH, '//span[@class="a-price-whole"]')
        # Find all product image elements
        imgs = driver.find_elements(By.XPATH, '//img[@class="s-image"]')
        
        # Loop through titles, prices, and images simultaneously
        for title_el, price_el, img_el in zip(titles, prices, imgs):
            title = title_el.text.strip()  # Get clean text of product title
            price = price_el.text.strip()  # Get clean text of product price
            img = img_el.get_attribute("src")  # Get image URL
            
            # Append product info as a dictionary to the list
            item_list.append({
                "title": title,
                "price": price,
                "img": img
            })
        
        # Return the list after scraping one page (you can extend this to paginate)
        return item_list
