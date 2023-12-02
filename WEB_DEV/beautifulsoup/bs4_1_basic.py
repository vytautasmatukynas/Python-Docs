from bs4 import BeautifulSoup
# if xml then import lxml and soup = BeautifulSoup(data, 'lxml')


with open("website.html", encoding="utf-8") as file:
    data = file.read()

soup = BeautifulSoup(data, 'html.parser')

print(soup.title)
print("\n")
print(soup.title.name)
print("\n")
print(soup.title.string)
print("\n")

print(soup.a)
print("\n")

print(soup.h1)
print("\n")

print(soup)
print("\n")
print(soup.prettify())
print("\n")



