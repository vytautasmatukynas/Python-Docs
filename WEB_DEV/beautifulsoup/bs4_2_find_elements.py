from bs4 import BeautifulSoup
# if xml then import lxml and soup = BeautifulSoup(data, 'lxml')


with open("website.html", encoding="utf-8") as file:
    data = file.read()

soup = BeautifulSoup(data, 'html.parser')

all_tags = soup.find_all(name="h1")
print(all_tags)

all_tags = soup.find_all(name="p")
print(all_tags)

all_tags = soup.find_all(name="a")
print(all_tags)

for tag in all_tags:
    # get all elements as text.
    print(tag.getText())
    # get href of elements. ".get()" gets value of all attributes.
    print(tag.get("href"))

# find element by tag name and id
heading = soup.find(name="h1", id="name")
print(heading)
# find element by tag name and class
heading = soup.find(name="h3", class_="heading")
print(heading.getText())
print(heading.name)
print(heading.get("class"))

# find <a> wich is in <p>, syntax like css
company_url = soup.select_one(selector="p a")
print(company_url)
name = soup.select_one(selector="#name")
print(name)

# select item woth class heading
headings = soup.select(".heading")
print(headings)
