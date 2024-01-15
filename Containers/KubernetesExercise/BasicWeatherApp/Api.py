import requests


# API integration:
def get_weather(location):
    key = '3407b726ce32e0fdd2588dc7b3058dd3'
    # the result is for every 3 hours, so I need for 7 days :
    # 24 / 3 = 8 * 7 = 56 and then:
    # filter the result for every day so : min temp is night temp and max temp is day temp
    cnt = 56
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={location}&cnt={cnt}&APPID={key}'
    weather = requests.get(url).json()
    print(weather)
    return relevant_info_weather(weather)


def relevant_info_weather(weather):
    weather_info = []
    if weather.get('cod') == '404':
        weather_info.append({'cod': weather.get('cod')})
        return weather_info
    elif weather.get('cod') == '200':
        cod = weather.get('cod')
        day = None
        night = None
        country = weather['city']['country']
        for item in weather['list']:
            dt = item['dt_txt']
            date = dt.split(' ')[0]
            time = dt.split(' ')[1]
            humidity = item['main']['humidity']
            temp = int(item['main']['temp'] - 273.15)
            if time == '12:00:00':
                day = temp
            elif time == '21:00:00':
                night = temp
                weather_info.append({'cod': cod, 'date': date, 'day_temp': day, 'night_temp': night, 'humidity': humidity})
                day = None
                night = None
        print(weather_info)
        return weather_info






if __name__ == '__main__':
    print(get_weather('London'))
