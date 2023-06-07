import requests
from datetime import datetime
import sys

class WeatherException(Exception):
    pass

def get_weather(lat: str, lon: str, date: str, time: str):
  url = 'https://archive-api.open-meteo.com/v1/archive?timezone=Europe%2FBerlin'
  params = {
      'latitude': lat,
      'longitude': lon,
      'start_date': date,
      'end_date': date,
      'hourly': 'weathercode,temperature_2m,precipitation,rain,snowfall'
  }

  response = requests.get(url, params=params)
  weather_data = response.json()

  if weather_data.get('error', False) == True:
    raise WeatherException(weather_data['reason'])
  
  try:
    date_format = '%Y-%m-%dT%H:%M'
    request_time = datetime.strptime(date + 'T' + time, date_format)

    matching_date_diff = sys.maxsize
    matching_date_idx = None
    for idx, d in enumerate(weather_data['hourly']['time']):
      diff = datetime.strptime(d, date_format) - request_time
      diff_minutes = abs(divmod(diff.total_seconds(), 60)[0])
      if diff_minutes < matching_date_diff:
        matching_date_diff = diff_minutes
        matching_date_idx = idx

    weather = {
      'units': weather_data['hourly_units'],
      'weather': {k: v[matching_date_idx] for k, v in weather_data['hourly'].items()}
    }
  except Exception as e:
    raise WeatherException('Weather parsing error')

  return weather


if __name__ == '__main__':
  print(get_weather(lat='51.34', lon='12.37', date='2023-05-04', time='23:40'))
  # WMO Codes: https://www.meteopool.org/de/encyclopedia-wmo-ww-wx-code-id2