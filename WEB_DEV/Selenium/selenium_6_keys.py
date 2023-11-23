from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


URL = "https://en.wikipedia.org/wiki/Wikipedia"

driver = webdriver.Chrome()

driver.get(URL)

# search for "search" input and input text to search input
search_open = driver.find_element(By.XPATH, "/html/body/div[1]/div/header/div[2]/div/a")
search_open.click()
search = driver.find_element(By.NAME, "search")

# pres any key you want, at this point its ENTER
search.send_keys("Lithuania")

# re-finding the search element after clicking on the search button,
# and before sending the ENTER key. This should ensure that the element
# is still attached to the DOM
search = driver.find_element(By.NAME, "search")
search.send_keys(Keys.ENTER)

click_on_found_item = driver.find_element(By.LINK_TEXT, 'Lithuania')

click_on_found_item.click()

sleep(1000)