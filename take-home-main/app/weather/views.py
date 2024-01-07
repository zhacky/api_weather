import datetime
import os
import json

import requests
from django.shortcuts import render


def weather_index(request):
    API_KEY = os.environ.get('WEATHER_API_KEY')
    # source: https://openweathermap.org/current#builtin
    # https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}

    # source: https://openweathermap.org/forecast5#geo5
    # https:?/api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}
    # icon : https://openweathermap.org/img/wn/{{icon}}@2x.png
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    forecast_weather_url = 'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric'

    if request.method == 'POST':
        city = request.POST['city']
        weather_data, daily_forecast = fetch_weather_and_forecast(api_key=API_KEY,
                                                                  current_weather_api=current_weather_url,
                                                                  forecast_weather_api=forecast_weather_url, city=city)
        context = {
            'weather_data': weather_data,
            'daily_forecast': daily_forecast
        }
        return render(request, 'weather.html', context)
    else:
        return render(request, 'weather.html')


def fetch_weather(*, api_key, current_weather_api, city):
    response = requests.get(current_weather_api.format(city=city, api_key=api_key)).json()
    return response


def fetch_weather_and_forecast(*, api_key, current_weather_api, forecast_weather_api, city):
    response = fetch_weather(api_key=api_key, current_weather_api=current_weather_api, city=city)
    lat, lon = '8.477217', '124.645920'
    forecast_response = fetch_forecast(api_key=api_key, forecast_weather_api=forecast_weather_api, lat=lat, lon=lon)

    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'], 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon']
    }

    daily_forecast = []

    for i, daily in enumerate(forecast_response['list']):
        recommendations = {2: '⛈️🧥', 3: '🌨️👘', 5: '☔️🧙‍♀️', 6: '❄️☃️', 7: '🌋👷️', 8: '👗👔'}
        # if i % 8 == 0:
        if i:
            # int(daily['weather'][0]['id'])
            daily_forecast.append({
                'outfit': get_recommendation(int(daily['weather'][0]['id']), outfits=recommendations),
                'day': datetime.datetime.fromtimestamp(daily['dt']).strftime(format='%A'),
                'full_dt': daily['dt_txt'],
                'min_temp': round(daily['main']['temp_min'], 2),
                'max_temp': round(daily['main']['temp_max'], 2),
                'description': daily['weather'][0]['description'],
                'icon': daily['weather'][0]['icon']
            })

    return weather_data, daily_forecast


def fetch_forecast(*, api_key, forecast_weather_api, lat, lon):
    response = requests.get(forecast_weather_api.format(lat=lat, lon=lon, api_key=api_key)).json()
    return response


def get_recommendation(weather_id, outfits):
    try:
        key = int((weather_id / 100) % 10)
        return outfits[key]
    except KeyError:
        return outfits[8]
