from datetime import date, datetime
import requests
from bs4 import BeautifulSoup as bs
from config_data.config import load_config

# Константы
CONFIG = load_config()
URL = 'https://lk.mubint.ru/schedule/report/'
MONTHS = {"Январь": 1,
          "Февраль": 2,
          "Март": 3,
          "Апрель": 4,
          "Май": 5,
          "Июнь": 6,
          "Июль": 7,
          "Август": 8,
          "Сентябрь": 9,
          "Октябрь": 10,
          "Ноябрь": 11,
          "Декабрь": 12
          }
CSRFTOKEN = CONFIG.parser.cfsrtoken


def get_schedule(group, amount_days=7) -> list:
    # Создаю запрос и тело запроса
    s = requests.session()
    payload = {
        # Действителен до октября 2024 (можно взять из браузера)
        'csrfmiddlewaretoken': CSRFTOKEN,
        'gruppa': group,

    }

    headers = {
        # Действителен до октября 2024 (можно взять из браузера)
        'Cookie': f'csrftoken = {CSRFTOKEN}'
    }

    req = s.post(URL, headers=headers, data=payload)
    # Парсинг
    soup = bs(req.text, "html.parser")
    table = soup.findAll('table', class_='table table-sm')
    schedule = []
    cur_year = str(datetime.now().year)
    day_schedule = {}
    lesson_number = 0
    for info in table:
        for text in info.text.split('\n'):
            if text.startswith(cur_year):
                lesson_number = 0
                schedule.append(day_schedule)
                _date = text.split(',')[:-1]
                year = int(_date[0])
                month = MONTHS[_date[1].split()[0]]
                day = int(_date[1].split()[1])
                day_schedule = {'date': date(year=year, month=month, day=day)}
            elif len(text) > 4 and text[0].isdigit() and (text[2] == ':' or text[1] == ":"):
                lesson_number += 1
                time_start, time_stop = text.split('-')
                time_start = int(time_start.split(":")[0]) * 3600 + int(time_start.split(":")[1]) * 60
                time_stop = int(time_stop.split(":")[0]) * 3600 + int(time_stop.split(":")[1]) * 60
                day_schedule.setdefault('events', dict())[lesson_number] = {'time_start': time_start,
                                                                            'time_stop': time_stop}
            elif not text.isspace() and day_schedule.get(
                    'events') and not text.startswith(group) and len(text) > 1:
                if day_schedule.get('events', {}).get(lesson_number, {}).get('title'):
                    day_schedule['events'][lesson_number]['title'] += text + " "
                else:
                    day_schedule['events'][lesson_number]['title'] = text + " "
    schedule = schedule[1:amount_days + 1]

    return schedule


def get_human_time(time):
    hours = time // 3600
    minutes = (time // 60) % 60
    return hours, minutes


if __name__ == "__main__":
    for d in get_schedule("22-ИБ111", amount_days=31):
        print(d)
    print(get_human_time(44100))
