from bs4 import BeautifulSoup
import requests

response = requests.get("https://news.ycombinator.com/")
webpage = response.text

soup = BeautifulSoup(webpage, "html.parser")

heading = soup.find(name="span", class_="titleline")
print(heading)
print("\n")
print(heading.getText())
print("\n")

# select <a>
anchor = heading.select(selector="a")
print(anchor)
print("\n")

# get href from <a>
print(heading.select(selector="a")[0].get("href"))
print("\n")

# get score(points)
score = soup.find(name="span", id="score_35385339")
print(score.getText())

