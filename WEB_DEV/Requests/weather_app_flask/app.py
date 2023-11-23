from flask import Flask, request, render_template
import requests

app = Flask(__name__)

API_ULR = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "c9dc93a19153c2fd0758094775ba50cc"


@app.route('/', methods=['GET', 'POST'])
def home():
    CARD_TEXT = "Search for weather conditions in your location."
    LOCATION = "None"
    TEMP = "None"
    WEATHER = "None"
    WIND = "None"
    
    if request.method == 'POST': 
        try:
            LOCATION = request.form['Search'].capitalize()

            param_url = {
                "q": LOCATION,
                "units": "metric",
                "appid": API_KEY,
            }

            response = requests.get(url=API_ULR, params=param_url)

            data = response.json()

            CARD_TEXT = f'Current weather conditions in location "{LOCATION}":'
            TEMP = data["main"]['temp']
            WIND = str(data["wind"]['speed']) + "m/s"
            WEATHER = data["weather"][0]['main']
            
            return render_template('index.html', location=LOCATION, temp=TEMP, wind=WIND, weather=WEATHER, card_text=CARD_TEXT)
        
        except KeyError:
            CARD_TEXT = "Search for weather conditions in valid location."
            LOCATION = "None"
            TEMP = "None"
            WEATHER = "None"
            WIND = "None"
            
            return render_template('index.html', location=LOCATION, temp=TEMP, wind=WIND, weather=WEATHER, card_text=CARD_TEXT)
            
    return render_template('index.html', location=LOCATION, temp=TEMP, wind=WIND, weather=WEATHER, card_text=CARD_TEXT)
        

if __name__ == "__main__":
    app.run(debug=True)