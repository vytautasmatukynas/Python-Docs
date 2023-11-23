from bs4 import BeautifulSoup
import requests

response = requests.get("https://news.ycombinator.com/")
webpage = response.text

soup = BeautifulSoup(webpage, "html.parser")

# find all elements and append it to list
heading = soup.find_all(name="span", class_="titleline")

art_text = []
art_link = []
score_list = []

for artical_tag in heading:
    anchor = artical_tag.getText()
    art_text.append(anchor)
    link = artical_tag.select(selector="a")[0].get("href")
    art_link.append(link)

score = soup.find_all(name="span", class_="score")

for artical_score in score:
    score_list.append(artical_score.getText())

print(art_text)
print("\n")

# get all scores and split to just get number
score_number_list = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]
print(score_number_list)
print("\n")

# get highest score index
top_points_index = score_number_list.index(max(score_number_list))

# print name/link and highest points for article with top points
print(f"{art_text[top_points_index]}: {art_link[top_points_index]} with {score_number_list[top_points_index]} points")

