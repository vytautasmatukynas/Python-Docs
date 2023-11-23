from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
from time import sleep


URL = "https://www.aruodas.lt/"
CITY = input("City name: ")
LOW_PRICE = input("Price from: ")
HIGH_PRICE = input("Price to: ")
LOW_SIZE = input("Square meters from: ")
HIGH_SIZE = input("Square meters to: ")
ATSTUMAS = input("Range from city center: ")

driver = webdriver.Chrome()

driver.get(URL)
sleep(1)

try:
    select_cookies = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
    select_cookies.click()
    sleep(1)
except:
    pass

click_empty_space = driver.find_element(By.XPATH, '//*[@id="boxSearches"]')

# select list items to find houses and fills search inputs with your input values
select_busto_tipas = driver.find_element(By.XPATH, '//*[@id="display_text_obj"]')
select_busto_tipas.click()
sleep(0.5)
select_namai = driver.find_element(By.XPATH, '//*[@id="options_obj"]/ul/li[2]/label')
select_namai.click()

click_empty_space.click()
sleep(0.5)

select_namo_tipas = driver.find_element(By.XPATH, '//*[@id="display_text_FBuildingType"]')
select_namo_tipas.click()
sleep(0.5)
select_gyvenamasis = driver.find_element(By.XPATH, '//*[@id="options_FBuildingType"]/ul/li[1]/label/input')
select_gyvenamasis.click()
sleep(0.5)

click_empty_space.click()
sleep(0.5)

select_irengimo_tipas = driver.find_element(By.XPATH, '//*[@id="display_text_FHouseState"]')
select_irengimo_tipas.click()
sleep(0.5)
select_irengtas = driver.find_element(By.XPATH, '//*[@id="options_FHouseState"]/ul/li[1]/label/input')
select_irengtas.click()
sleep(0.5)

click_empty_space.click()
sleep(0.5)

fill_plotas_nuo = driver.find_element(By.XPATH, '//*[@id="input_FAreaOverAllMin"]')
fill_plotas_nuo.send_keys(LOW_SIZE)
sleep(0.5)
fill_plotas_nuo = driver.find_element(By.XPATH, '//*[@id="input_FAreaOverAllMax"]')
fill_plotas_nuo.send_keys(HIGH_SIZE)
sleep(0.5)

press_city_input = driver.find_element(By.XPATH, '//*[@id="display_FRegion"]')
press_city_input.click()
sleep(0.5)
fill_city_name = driver.find_element(By.XPATH, '//*[@id="filterInput_FRegion"]')
fill_city_name.send_keys(CITY)
sleep(0.5)
fill_city_name.send_keys(Keys.ENTER)
sleep(0.5)

fill_kaina_nuo = driver.find_element(By.XPATH, '//*[@id="input_FPriceMin"]')
fill_kaina_nuo.send_keys(LOW_SIZE)
sleep(0.5)
fill_kaina_iki = driver.find_element(By.XPATH, '//*[@id="input_FPriceMax"]')
fill_kaina_iki.send_keys(HIGH_PRICE)
sleep(0.5)


press_atstumas_iki = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[4]/div/form/div/div[1]/div/div[1]/div[1]/div[5]/div/div[1]/div[5]/div')
press_atstumas_iki.click()
sleep(0.5)
press_atstumas_iki = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[4]/div/form/div/div[1]/div/div[1]/div[1]/div[5]/div/div[2]/div[1]/span/input')
press_atstumas_iki.send_keys(ATSTUMAS)
press_atstumas_iki.send_keys(Keys.ENTER)
sleep(1)

# get data of found houses
get_loc = driver.find_elements(By.CSS_SELECTOR, "div .list-row-v2 h3 a")
loc = [i.text.replace("\n", ", ") for i in get_loc]
print(loc)

kainos_get = driver.find_elements(By.CSS_SELECTOR, "div .list-row-v2 .list-item-price-v2")
kainos = [i.text for i in kainos_get]
print(kainos)

get_link = driver.find_elements(By.CSS_SELECTOR, "div .list-row-v2 h3 a")
link = [i.get_attribute("href") for i in get_link]
print(link)

plotas_title = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[1]/div[8]/div[3]/div/div[3]")
print(plotas_title.text)

plotas_get = driver.find_elements(By.CSS_SELECTOR, "div .list-AreaOverall-v2")
plotas = [i.text for i in plotas_get if i.text != "" and i.text != f'{plotas_title.text}']
print(plotas)

zemes_plotas_title = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[1]/div[8]/div[3]/div/div[4]")
print(zemes_plotas_title.text)

zemes_plotas_get = driver.find_elements(By.CSS_SELECTOR, "div .list-AreaLot-v2")
zemes_plotas = [i.text for i in zemes_plotas_get if i.text != "" and i.text != f'{zemes_plotas_title.text}']
print(zemes_plotas)

# house_dict = {i + 1: {"Vieta": loc[i].split("\n"),
#                       "Kaina": kainos[i],
#                       "Plotas": plotas[i],
#                       "Sklypo plotas (a)": zemes_plotas[i],
#                       "Nuoroda i skelbima": link[i]} for i in range(len(loc))}

# create file with found houses
with open(f"selenium_scrape_house_list_to_txt-{CITY}.txt",
          'w',
          encoding="utf-8") as file:
    for i in range(len(loc)):
        file.write(f"{i + 1}. Adresas: {loc[i]};\n"
                   f"Kaina: {kainos[i]};\n"
                   f"Plotas: {plotas[i]};\n"
                   f"Sklypo plotas: {zemes_plotas[i]};\n"
                   f"Nuoroda i skelbima: {link[i]}.\n\n")