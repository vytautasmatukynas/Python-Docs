from selenium import webdriver
from selenium.webdriver.common.by import By


URL = "http://orteil.dashnet.org/experiments/cookie/"

driver = webdriver.Chrome()

driver.get(URL)

cookie_img = driver.find_element(By.ID, 'cookie')

while True:
    cookie_img.click()


