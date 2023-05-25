from datetime import datetime, timedelta

import requests
import pytz

from bs4 import BeautifulSoup as bs


def get_cf_contest_list():
    response = requests.get('https://codeforces.com/contests?complete=true')
    soup = bs(response.text, 'html.parser')
    contestList = soup.select('.datatable')[0]
    table = contestList.find('table')
    rowList = table.find_all('tr')[1:]
    res = []
    for row in rowList:
        columnList = row.find_all('td')
        contestId = row['data-contestid']
        nameTd = columnList[0]
        timeTd = columnList[2]
        name = nameTd.text.strip()
        timeLink = timeTd.find('a')
        timeLink = timeLink['href']
        day = timeLink[timeLink.find('day=') + 4:timeLink.find('&month=')]
        month = timeLink[timeLink.find('month=') + 6:timeLink.find('&year=')]
        year = timeLink[timeLink.find('year=') + 5:timeLink.find('&hour=')]
        hour = timeLink[timeLink.find('hour=') + 5:timeLink.find('&min=')]
        minute = timeLink[timeLink.find('min=') + 4:timeLink.find('&sec=')]
        time = datetime(int(year), int(month), int(day), int(hour), int(minute)) + timedelta(hours=+3)
        # make utc time
        time = time.replace(tzinfo=pytz.timezone('Asia/Dhaka'))
        contestLink = f"https://codeforces.com/contests/{contestId}"
        res.append([name, contestLink, time])
    return res


def get_at_contest_list():
    response = requests.get('https://atcoder.jp/contests/')
    soup = bs(response.text, 'html.parser')
    contest_table_div = soup.select_one('div#contest-table-upcoming')
    contest_table = contest_table_div.select_one('table.table')
    contest_list = contest_table.select('tr')[1:]
    res = []
    for contest in contest_list:
        timeLink = contest.select_one('a')['href']
        nameLinkObj = contest.select('a')[1]
        iso_time = timeLink.split('=')[1].split('&')[0]
        contest_time = datetime.strptime(iso_time, '%Y%m%dT%H%M') + timedelta(hours=-3)
        # make utc time
        contest_time = contest_time.replace(tzinfo=pytz.timezone('Asia/Dhaka'))
        contestLink = f"https://atcoder.jp{nameLinkObj['href']}"
        res.append([nameLinkObj.text.strip(), contestLink, contest_time])
    return res


def convert_time_str(time_str):
    week_days = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6
    }
    day_str = time_str.split(' ')[0]
    time_str = ' '.join(time_str.split(' ')[1:])
    day_time_obj = datetime.strptime(day_str + ' ' + time_str, '%A %I:%M %p %Z')
    current_time = datetime.utcnow()
    days_until_day = (week_days[day_str] - current_time.weekday()) % 7
    if days_until_day == 0 and current_time.time() > day_time_obj.time():
        days_until_day = 7

    # Calculate the date of the next occurrence of the specified day and time
    next_day = current_time + timedelta(days=days_until_day)
    next_day = next_day.replace(hour=day_time_obj.hour, minute=day_time_obj.minute, second=day_time_obj.second,
                                microsecond=day_time_obj.microsecond)
    return next_day


def get_lt_contest_list():
    response = requests.get('https://leetcode.com/contest/')
    soup = bs(response.text, 'html.parser')
    contest_list = soup.select_one('.swiper-wrapper')
    res = []
    for contest in contest_list:
        link = contest.select_one('a')['href']
        name = contest.select_one('.truncate').text.strip()
        time_str = contest.select_one(r'.text-\[14px\]').text
        time = convert_time_str(time_str) + timedelta(hours=+6)
        # make utc time
        time = time.replace(tzinfo=pytz.timezone('Asia/Dhaka'))
        contest_link = f"https://leetcode.com{link}"
        res.append([name, contest_link, time])
    return res
