import requests

# request.get() - ask for piece of data from server and get it.
# request.post() - give data to server. Create piece of data.
# request.put() - change an existing piece of data.
# request.delete() - delete an existing piece of data.

# uld to requests_API_SMS_EMAIL https://sunrise-sunset.org/api
LAT = 51.507351
LNG = -0.127758
param = {
    "lat": LAT,
    "lng": LNG,
    "formatted": 0,
}

# "params=" adds parameters to requests_API_SMS_EMAIL
response = requests.get("https://api.sunrise-sunset.org/json", params=param)
response.raise_for_status()

data = response.json()
print(data)

# sprint sunrise
sunrise = data["results"]["sunset"]
print(sunrise)

# split string and create list of split strings
sunrise = data["results"]["sunset"].split("T")
sunrise_split_2 = sunrise[1].split("+")

print(sunrise[1])
print(sunrise_split_2[0])

# OR

sunrise = data["results"]["sunset"].split("T")[1].split("+")[0]
print(sunrise)

