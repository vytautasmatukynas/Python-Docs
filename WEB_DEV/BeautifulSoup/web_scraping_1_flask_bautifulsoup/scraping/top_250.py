import requests
from bs4 import BeautifulSoup
import asyncio

# url to IMDB top 250 movies
URL = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
# unlock url from giving error forbidden 403. With headers URL now thinks that your browsing like human in web browser.
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}

# get data from URL
response = requests.get(URL, headers=HEADERS)
data = response.text
# parse URL
soup = BeautifulSoup(data, "html.parser")


class topClass():
    async def movies_names(self) -> list:
        # get movie names to imdb
        url_data_movie = soup.select(
            selector="a", class_="ipc-title-link-wrapper")
        # data list
        movies_names_cleaned = [item.getText().split(". ")[1]
                                for item in url_data_movie if item.getText() != "" and ". " in item.getText()]

        return movies_names_cleaned

    async def movies_link(self) -> list:
        # get movie links to imdb
        url_data_movie = soup.select(
            selector="a", class_="ipc-title-link-wrapper")
        # get movies links
        movies_links_cleaned = [link.get("href")
                                for link in url_data_movie if "title" in link.get("href")]

        return movies_links_cleaned[1:-1][::2]

    async def movies_img(self) -> list:
        # get img links
        url_data_img = soup.select(selector="img", class_="ipc-image")
        # data list
        img_cleaned = [img.get("src")
                       for img in url_data_img if "https://" in img.get("src")]

        return img_cleaned

    async def movies_rating(self) -> list:
        # get movie rating
        url_data_rating = soup.select(
            selector="span",
            class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating")
        # get movies rating
        rating_cleaned = [rating.get("aria-label").replace("IMDb", "IMDB")
                          for rating in url_data_rating if rating.get("aria-label") != None]

        return rating_cleaned

    async def zip_data(self) -> list:
        global movies_zipped_data

        task_1 = asyncio.create_task(self.movies_names())
        task_2 = asyncio.create_task(self.movies_link())
        task_3 = asyncio.create_task(self.movies_img())
        task_4 = asyncio.create_task(self.movies_rating())

        value_1 = await task_1
        value_2 = await task_2
        value_3 = await task_3
        value_4 = await task_4

        movies_zipped_data = list(zip(value_1, value_2, value_3, value_4))

        return movies_zipped_data

    def data(self) -> dict:
        asyncio.run(self.zip_data())

        movies_info = {index:
                           {"number": index,
                            "name": item[0],
                            "link": "https://www.imdb.com/" + item[1],
                            'img': item[2],
                            "rating": item[3]}
                       for index, item in enumerate(movies_zipped_data, 1)
                       }

        return movies_info
