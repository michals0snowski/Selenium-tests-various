from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up WebDriver
service_obj = Service(r"<chromedriver.exe path>")
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service_obj, options=options)

# Navigate to the page
driver.get("https://www.olx.pl/antyki-i-kolekcje/antyki/") #custom product cathegory url

# Wait for cookie consent and click
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#onetrust-accept-btn-handler'))).click()

# Sort by price
sorting_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.css-u2fqob')))
sorting_button.click()
driver.find_elements(By.CSS_SELECTOR, '[data-testid="sorting-option"]')[2].click()

# Wait for all product items to be loaded
product_items = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.css-rc5s2u')))

# List to store prices
prices = []

# Iterate through each product item
for item in product_items:
    # Check if the item contains "Wyróżnione"
    featured = item.find_elements(By.CSS_SELECTOR, '[data-testid="adCard-featured"]')
    if not featured:
        # Find the price element and extract the text
        price_element = item.find_element(By.CSS_SELECTOR, '[data-testid="ad-price"]')
        price = price_element.text.replace(' zł', '').replace('\ndo negocjacji', '').replace(' ', '').replace(',', '.')
        prices.append(price)

# Assert that prices are sorted
assert prices == sorted(prices)

# Output the list of prices
print(prices)

# Close the WebDriver
driver.quit()