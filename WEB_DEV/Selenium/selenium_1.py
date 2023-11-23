from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

URL = "https://www.amazon.com/Storage-Plastic-Stackable-Organizer-Containers/dp/B08FRR2YSN/?_encoding=UTF8&pd_rd_w=5C5V8&content-id=amzn1.sym.97f98749-3e11-4b97-9261-bb265d6c9962&pf_rd_p=97f98749-3e11-4b97-9261-bb265d6c9962&pf_rd_r=H290BNKJHVZ3SP100PE2&pd_rd_wg=A8WJm&pd_rd_r=727f00ff-93a6-40fb-897c-22eb768adf6f&ref_=pd_gw_trq_ed_15owhogo"

# chrome_driver_path = 'C:\Program Files (x86)\chrome_engine\chromedriver.exe'
# driver = webdriver.Chrome(executable_path=chrome_driver_path)

# # Error FIX with service: "DeprecationWarning: executable_path has been deprecated, please pass in a Service object
# # driver = webdriver.Chrome(executable_path=chrome_driver_path)".
chrome_driver_path = Service('C:\Program Files (x86)\chrome_engine\chromedriver.exe')
driver = webdriver.Chrome(service=chrome_driver_path)

driver.get(URL)
# CLASS_NAME is by class, ID is by id... look docs or google it for all others.
price = driver.find_element(By.CLASS_NAME, "a-offscreen")

# get_attribute("outerHTML") gets all tag and get_attribute("innerHTML") gets just text
print(price.get_attribute("innerHTML"))

# price = driver.find_elements(By.TAG_NAME, "span")
# for item in price:
#     print(item.get_attribute("innerHTML"))
