from scraping.top_250 import topClass
from scraping.moviemeter import meterClass


def moviemeter():
    data = meterClass().data()
    return print(data)

def top250():
    data = topClass().data()
    return print(data)


if __name__ == "__main__":
    moviemeter()
    top250()
