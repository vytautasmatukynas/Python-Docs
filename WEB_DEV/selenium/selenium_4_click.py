from selenium import webdriver
from selenium.webdriver.common.by import By


URL = "https://en.wikipedia.org/wiki/Main_Page"

driver = webdriver.Chrome()

driver.get(URL)

# article_count = driver.find_element(By.CSS_SELECTOR, "#articlecount a")
# print(article_count.text)
# # "click" clicks on this link or text or button or entry
# article_count.click()

# opens webpage and click on link "Wikipedia"
link_to_view_history = driver.find_element(By.LINK_TEXT, "Wikipedia")
link_to_view_history.click()
