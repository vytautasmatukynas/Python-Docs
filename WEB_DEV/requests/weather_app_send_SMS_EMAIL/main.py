import smtplib as smtp

import requests
from twilio.rest import Client

# twilio info
ACCOUNT_SID = "Your SID"
AUTH_TOKEN = "Your TOKEN"

# API info
API_ULR = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "YOUR_KEY"
LOCATION = "Kaunas, LT"  # enter any city

param_url = {
    "q": LOCATION,
    "units": "metric",
    "appid": API_KEY,
}

response = requests.get(url=API_ULR, params=param_url)

data = response.json()

TEMP = data["main"]['temp']
WIND = data["wind"]['speed']


def send_sms(tempeture, wind_speed):
    # send sms with twilio
    message = None
    DEFAULT_NUMBER = '+00000'
    to_number = '+00000'

    try:

        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        message = client.messages.create(
            body=f'Todays tempeture: {tempeture}C, wind speed: {wind_speed}m/s.',
            from_=DEFAULT_NUMBER,
            to=to_number
        )

    except:
        raise Exception("Error, check your code")

    finally:
        if message != None:
            print(message.status)


def send_email(tempeture, wind_speed):
    # send email with smtplib
    con = None

    try:
        # send email from gmail to gmail, you can change email providers, just SMTP will be different.
        form_email = "email-name@gmail.com"
        DEFAULT_EMAIL = "email-name@gmail.com"
        DEFAULT_PSW = "password"
        
        
        # create object from SMTP class
        with smtp.SMTP("smtp.gmail.com") as con:
            # tls - transport layour security. Encrypts email message.
            con.starttls()

            con.login(user=DEFAULT_EMAIL, password=DEFAULT_PSW)

            # after "Subject" you need to write "\n\n" and then your message.
            con.sendmail(from_addr=DEFAULT_EMAIL,
                         to_addrs=form_email,
                         msg=f"Subject:Weather today.\n\n"
                             f"Todays temperature: {tempeture}C, wind speed: {wind_speed}m/s.")

    except:
        raise Exception("Error, check your code")

    finally:
        if con != None:
            con.close()


send_sms(TEMP, WIND)
send_email(TEMP, WIND)