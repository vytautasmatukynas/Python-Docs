import smtplib as smtp

import requests
from twilio.rest import Client

# launch this app.py in "https://www.pythonanywhere.com/", set time when you want to get email or sms and ir will start
# app.py at that time.

API_ULR = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "c9dc93a19153c2fd0758094775ba50cc"
LOCATION = "Kaunas, LT"  # enter any city

param_url = {
    "q": LOCATION,
    "units": "metric",
    "appid": API_KEY,
}

response = requests.get(url=API_ULR, params=param_url)

data = response.json()

tempeture = data["main"]['temp']
wind_speed = data["wind"]['speed']


def send_sms(temp, wind):
    # send sms with twilio
    print(temp, wind)

    message = None

    try:
        ACCOUNT_SID = "Your SID"
        AUTH_TOKEN = "Your TOKEN"

        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        message = client.messages.create(
            body=f'Todays tempeture: {temp}C, wind speed: {wind}m/s.',
            from_='+00000',
            to='+00000'
        )

    except:
        raise Exception("Error, check your code")

    finally:
        if message != None:
            print(message.status)


def send_email(temp, wind):
    print(temp, wind)

    con = None

    try:
        # send email from gmail to gmail, you can change email providers, just SMTP will be different.
        my_email = "email-name@gmail.com"
        to_email = "email-name@gmail.com"
        psw = "password"

        # create object from SMTP class
        with smtp.SMTP("smtp.gmail.com") as con:
            # tls - transport layour security. Encrypts email message.
            con.starttls()

            con.login(user=my_email, password=psw)

            # after "Subject" you need to write "\n\n" and then your message.
            con.sendmail(from_addr=my_email,
                         to_addrs=to_email,
                         msg=f"Subject:Weather today.\n\n"
                             f"Todays temperature: {temp}C, wind speed: {wind}m/s.")

    except:
        raise Exception("Error, check your code")

    finally:
        if con != None:
            con.close()


send_sms(tempeture, wind_speed)
send_email(tempeture, wind_speed)
