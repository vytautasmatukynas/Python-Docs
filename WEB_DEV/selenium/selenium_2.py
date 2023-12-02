from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


URL = "https://www.python.org/"

driver = webdriver.Chrome()

driver.get(URL)

# Searches element by name
search_bar = driver.find_element(By.NAME, "q")
# Get attribute you want
print(search_bar.get_attribute("class"))
print(search_bar.get_attribute("placeholder"))

# Searches by element
logo = driver.find_element(By.CLASS_NAME, "python-logo")
# Get attribute you want
print(logo.size)

# Searches for element like in css
a_tag_doc_link = driver.find_element(By.CSS_SELECTOR, ".documentation-widget a")
# Get attribute you want
print(a_tag_doc_link.text)

# Searches for element by path. Just copy XPATH from browser. OP!
bug_link = driver.find_element(By.XPATH, "/html/body/div/footer/div[2]/div/ul/li[3]/a")
# Get attribute you want
print(bug_link.text)