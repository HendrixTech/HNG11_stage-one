from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

IP_API_KEY = '4d2670b83c374b'
WEATHER_API_KEY = 'a61ae98b33fd1b1b5cf5f0f09d2aa346'


def get_location_and_weather(ip):
    location_url = f'https://ipinfo.io/{ip}/json?token={IP_API_KEY}'
    location_res = requests.get(location_url)
    location_data = location_res.json()

    city = location_data.get('city', 'Unknown location')
    country = location_data.get('country', '')

    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'
    weather_res = requests.get(weather_url)
    weather_data = weather_res.json()

    if weather_data.get('main'):
        temp = weather_data['main']['temp']
    else:
        temp = 'Unknown'

    return city, country, temp


@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Guest')
    client_ip = request.remote_addr

    # if client_ip == '127.0.0.1':
    #     client_ip = '8.8.8.8'

    city, country, temp = get_location_and_weather(client_ip)
    message = f'Hello, {visitor_name}!, the temperature is {temp} degrees Celsius in {city}'

    response = {
        "client_ip": client_ip,
        "location": f"{city}",
        "greeting": message
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
