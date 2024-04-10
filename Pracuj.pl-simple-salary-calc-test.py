from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

service_obj = Service(r"<chromedriver.exe path>")
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service_obj, options=options)
driver.implicitly_wait(2)

driver.get("https://zarobki.pracuj.pl/kalkulator-wynagrodzen")

#Wait for the elements to be loaded
wait = WebDriverWait(driver, 5)

cookie_consent = driver.find_element(By.XPATH, '//*[@id="gp_cookie_agreements"]/div/div/div/div[3]/div/button[1]')
cookie_consent.click()

#Provide variable and gross to net switch
salary = 10000
earnings = driver.find_element(By.ID, "simple_calculator_salary").send_keys(f"{salary}")
net_check = driver.find_element(By.XPATH, '//*[@id="simple_calculator_type"]/span[2]/label').click()

#Submit
driver.find_element(By.XPATH, '//*[@id="simple_calculator_submit"]').click()

employment_contract = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/main/div/div[1]/div[1]/div/a/div[2]/div').text
mandate_contract = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/main/div/div[1]/div[2]/div/a/div[2]/div').text
contract_work = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/main/div/div[1]/div[3]/div/a/div[2]/div').text
b2b = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/main/div/div[1]/div[4]/div/a/div[2]/div').text

#Salary formatting
employment_contract = int(employment_contract.replace('zł', '').replace(' ', ''))
mandate_contract = int(mandate_contract.replace('zł', '').replace(' ', ''))
contract_work = int(contract_work.replace('zł', '').replace(' ', ''))
b2b = int(b2b.replace('zł', '').replace(' ', ''))

#Asserting net to gross salary calculations
assert employment_contract == round(salary * 1.4185)
assert mandate_contract == round(salary * 1.3843)
assert contract_work == round(salary * 1.1062)
assert b2b == round(salary * 1.2982)