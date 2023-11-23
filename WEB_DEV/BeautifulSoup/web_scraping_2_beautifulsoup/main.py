import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.imdb.com/list/ls055592025/")
data = response.text
print(data)

soup = BeautifulSoup(data, "html.parser")
url_data = soup.select(selector="h3", class_="lister-item-content")
print(url_data)

movies_names = []

for item in url_data:
    try:
        name = item.select(selector='a')
        print(name)
        items = (str(name).split(">"))[1].split("<")[0]
        print(items)
        movies_names.append(items)

    except IndexError:
        pass

print(movies_names)

# "enumerate(movies_names, 1)" starts number enumerating from 1
movies_list = [f"{index}. {name}" for index, name in enumerate(movies_names, 1)]
print(movies_list)

# print(movies_list)

with open('bs4_scrape_movie_list_to_txt.txt', 'w', encoding='utf-8') as file:
    for item in movies_list:
        file.write(f"{item}\n")
