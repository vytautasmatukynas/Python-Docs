import requests
from twilio.rest import Client
import os

# store sensitive data in ENV - in terminal write "set VARIABLE_NAME=VALUE"
# then with "os.environ.get("")" you can get your data from ENV. ENV data is STR.
# To see all ENV data you have to typer ENV in terminal.

# Get current temp in your location
URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = os.environ.get("API_KEY")

param_url = {
    "q": "Kaunas, LT",
    "units": "metric",
    "appid": API_KEY,
}

# twilio info
ACCOUNT_SID = os.environ.get("SID")
AUTH_TOKEN = os.environ.get("TOKEN")

response = requests.get(URL, params=param_url)
response.raise_for_status()
data = response.json()
temp = data["main"]['temp']
print(temp)

temp_high = False

if int(temp) < 10:
    # send sms
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages.create(
        body='DONT LEAVE HOME... OMG OMG',
        from_='+00000',
        to='+00000'
    )

    print(message.status)

else:
    temp_high = True

if temp_high:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages.create(
        body='GO OUTSIDE',
        from_='+00000',
        to='+00000'
    )

    print(message.status)