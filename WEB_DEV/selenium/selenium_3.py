from selenium import webdriver
from selenium.webdriver.common.by import By


URL = "https://www.python.org/"

driver = webdriver.Chrome()

driver.get(URL)

# get month and day of event
events_month_day = driver.find_elements(By.CSS_SELECTOR, ".event-widget time")
# get year of event
events_year = driver.find_elements(By.CSS_SELECTOR, ".event-widget time span")
# get name of event
event_names = driver.find_elements(By.CSS_SELECTOR, ".event-widget li a")

# 5 nearest upcoming event dict, using dict comprehension
events = {i + 1: {"date": events_year[i].get_attribute("innerHTML") + events_month_day[i].text,
                  "name": event_names[i].text}
          for i in range(len(events_month_day))}

# # or same loop as above like this
# for i in range(len(events_year)):
#     events[i + 1] = {
#         "date": events_year[i].get_attribute("innerHTML") + events_year[i].text,
#         "name": event_names[i].text
#     }

print(events)