"""
    1.get current date
        use datetime.date class
    2.get 4 tables from rusp.tpu
        use request lib
    3.find today timetable for 4 tables
        enter system of probability:
            Van_prob is 50%
            Ser_prob is 25%
            Tim_prob us 25%
        take into account some objects that there are in a timetable but it isn't for him
        create array of exceptions
        create algorithm
    4.compare them and do conclusion

"""

from icalendar import Calendar
import requests
import datetime


def do_plus(obj1, obj2):
    if obj1.hour != 3 and obj1.hour != 1:
        return datetime.time(obj1.hour + obj2.hour, obj1.minute + obj2.minute, obj1.second + obj2.second)
    else:
        return datetime.time(obj1.hour + obj2.hour, obj1.minute , obj1.second)


"""return dict of begging of lessons"""


def get_timetables(url, index):
    free_time = {}
    gmt = datetime.time(7, 20, 0)
    file_link = 'day{}.ics'.format(index)
    with open(file_link, 'wb') as file:
        quarry = requests.get(url)
        file.write(quarry.content)
    cal = Calendar.from_ical(open(file_link, 'rb') .read())
    for sub in cal.subcomponents:
        dt = sub['DTSTART'].dt
        time = str(do_plus(dt.time(), gmt))
        date = str(dt.date())
        try:
            free_time[date].add(time)
        except KeyError:
            free_time[date] = set()
    for key in free_time.keys():
        free_time[key] = list(free_time[key])
        free_time[key].sort()
    return free_time


def compare_date(f_d, s_d):
    if sum(list(map(int, f_d.split('-')))) >= sum(list(map(int, s_d.split('-')))):
        return True
    else:
        return False


timetable = {}
today = str(datetime.datetime.now().date())
times = ['08:30:00', '10:25:00', '12:40:00', '14:35:00', '16:30:00', '18:25:00']
urls = {
    'V_url': 'https://rasp.tpu.ru/export/ical.html?key=GAsDmK',
    'S_url': 'https://rasp.tpu.ru/export/ical.html?key=CqBLmd',
    'T_url': 'https://rasp.tpu.ru/export/ical.html?key=Y7zNKW',
}
V_timetable = get_timetables(urls['V_url'], 1)
S_timetable = get_timetables(urls['S_url'], 2)
T_timetable = get_timetables(urls['T_url'], 3)
suitable_time = {}
for date in V_timetable.keys():
    if compare_date(date, today):
        for time in times:
            V, T, S = 1, 75, 25
            if time not in V_timetable[date]:
                V = 0
            if time not in T_timetable[date]:
                T = 0
            if time not in S_timetable[date]:
                S = 0
            chance = V*(T + S)
            suitable_time[time] = chance
        timetable[str(date)] = suitable_time.copy()
days = list(timetable.keys())
days.sort()
for day in days:
    print(day)
    for time, choice in timetable[day].items():
        print('\t',time,'==',choice)

