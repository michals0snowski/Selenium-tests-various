import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service_obj = Service(r"<chromedriver.exe path>")
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service_obj, options=options)
driver.implicitly_wait(2)

driver.get("https://www.axa-assistance.pl/ubezpieczenie-turystyczne/")

# Wait for the elements to be loaded
wait = WebDriverWait(driver, 5)

cookie_reject = driver.find_element(By.ID, "onetrust-reject-all-handler")
cookie_reject.click()

# Wait for the element to be clickable
offer_checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'select2')))

# Scroll the element into view
driver.execute_script("arguments[0].scrollIntoView();", offer_checkbox)
# Click on the element
driver.execute_script("arguments[0].click();", offer_checkbox)

# Adding offer options
checkbox_ids = [
    'p_lt_zoneContent_pageplaceholder_p_lt_ctl01_Ipus_SupplementariesSelector_ucSinglePersonSupplementaries_rpSupplementaries_ctl00_rpSupplementaryVariants_ctl01_chSelected',
    'p_lt_zoneContent_pageplaceholder_p_lt_ctl01_Ipus_SupplementariesSelector_ucSinglePersonSupplementaries_rpSupplementaries_ctl01_rpSupplementaryVariants_ctl01_chSelected',
    'p_lt_zoneContent_pageplaceholder_p_lt_ctl01_Ipus_SupplementariesSelector_ucSinglePersonSupplementaries_rpSupplementaries_ctl02_rpSupplementaryVariants_ctl01_chSelected',
    'p_lt_zoneContent_pageplaceholder_p_lt_ctl01_Ipus_SupplementariesSelector_ucSinglePersonSupplementaries_rpSupplementaries_ctl03_rpSupplementaryVariants_ctl01_chSelected'
]

checkboxes = []

# Locating checkboxes by ID
for checkbox_id in checkbox_ids:
    checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, checkbox_id)))
    checkboxes.append(checkbox)

# Scroll the element into view
driver.execute_script("arguments[0].scrollIntoView();", checkboxes[0])

# Clicking on all checkboxes
for checkbox in checkboxes:
    driver.execute_script("arguments[0].click();", checkbox)

# Getting the prices
time.sleep(2)
offer_price = driver.find_element(By.XPATH, '/html/body/form/div[6]/div[6]/div[1]/table/tbody/tr[35]/td[3]/span').text
options_price = driver.find_element(By.XPATH, '//*[@id="form"]/div[6]/div[9]/div[1]/div/table/tbody/tr[13]/td[3]/span/span').text
final_price = driver.find_element(By.XPATH, '/html/body/form/div[7]/div[1]/span[2]').text

# Formating prices
final_price = float((final_price[:-3]).replace(',', '.'))
offer_price = float((offer_price[:-3]).replace(',', '.'))
options_price = float((options_price[:-3]).replace(',', '.'))

# Checking if the offer sums up
assert final_price == (offer_price + options_price)