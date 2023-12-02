import requests

# request.get() - ask for piece of data from server and get it.
# request.post() - give data to server. Create piece of data.
# request.put() - change an existing piece of data.
# request.delete() - delete an existing piece of data.

# get data from endpoint
response = requests.get(url="http://api.open-notify.org/iss-now.json")
print(response)
print(response.status_code)


# if you don't get 200(it's OKAY) and get error, then it writes what error it is
response.raise_for_status()

#get .json data as dict
data = response.json()
print(data)

data = response.json()["iss_position"]
print(data)

data = response.json()["iss_position"]["latitude"]
print(data)

data1 = response.json()["iss_position"]["longitude"]
print(data1)

iss_position = (data, data1)
print(iss_position)