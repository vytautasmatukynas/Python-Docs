import requests

# request.get() - ask for piece of data from server and get it.
# request.post() - give data to server. Create piece of data.
# request.put() - change an existing piece of data.
# request.delete() - delete an existing piece of data.

response = requests.get(url="https://api.kanye.rest/")
response.raise_for_status()

print(response.json())

text = response.json()['quote']

print(text)