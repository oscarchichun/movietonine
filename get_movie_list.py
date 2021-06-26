import requests
from bs4 import BeautifulSoup
import pprint

# cron job for e.g. 10:00 every Sat. and Sun.
# 0 10 * * 0,6 /Library/Frameworks/Python.framework/Versions/3.9/bin/python3 /Users/oscarchao/project/python/get_movie_list/get_movie_list.py

pp = pprint.PrettyPrinter(indent=4)

# niotv
movie_url = 'http://www.niotv.com/i_index.php?cont=mulity_promote'
r = requests.get(movie_url)
r.encoding = 'utf-8'

soup = BeautifulSoup(r.text, 'lxml')

result = []
link = []
domain = 'http://www.niotv.com/'
channel_code = {
    '衛視電影': '61',
    'HBO':'65',
    '東森洋片':'66',
    '好萊塢電影':'68',
    'FOX_Movies':'69',
    'CINEMAX':'70',
}

today_tags = soup.find_all('img', attrs={'class': 'i_icon'})
for today_tag in today_tags:
    time_tag = today_tag.find_parent('td', attrs={'class': 'copy_movietext'})
    time = time_tag.text.split(')')[1]
    if time[:5] != '21:00' and time[:2] != '20':
        continue

    genre_tag = time_tag.find_parent('tr').find_previous_sibling('tr')
    genre = genre_tag.text
    channel_tag = genre_tag.find_previous_sibling('tr')
    channel = channel_tag.text
    film_tag = channel_tag.find_previous_sibling('tr')
    film = film_tag.text.strip()
    result.append(f"{film} {channel} {channel_code.get(channel)} {time} {genre}")
    link.append(f"{domain}{film_tag.find('a', href=True)['href']}")

""" deprecated
channel_map= {'HBO電影台':'CH65','東森洋片台':'CH66','AXN動作台':'CH67','FOX MOVIES':'CH69','Cinemax':'CH70','好萊塢電影台':'CH68'}
# 開眼電影網 - 西片
movie_url = 'http://tv.atmovies.com.tw/tv/attv.cfm?action=todaytime'
r = requests.get(movie_url)
r.encoding = 'utf-8'

soup = BeautifulSoup(r.text, 'lxml')

result = []
tags = soup.find_all("td", string="21:00")
for tag2100 in tags:
    movie_title = tag2100.find_next_sibling("td").find("font", class_="at11").string
    channel_tag = tag2100.find_parent("table", class_="at9").find_previous_sibling("a")
    channel_name = channel_tag.string
    channel_num = channel_tag.find_previous_sibling("a").attrs['name']
    # print(channel_map[channel_name], channel_name, movie_title)
    result.append(f"{channel_map[channel_name]} {channel_name} {movie_title}")
"""

# Line Notify
# ref. https://www.learncodewithmike.com/2020/06/python-line-notify.html
#  === replace this with your token === #
token = "your_token"

url = "https://notify-api.line.me/api/notify"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/x-www-form-urlencoded"
}
result = "\n".join(result)
link = "\n\n".join(link)
params = {"message": f'\n{result}\n連結:\n{link}\n查看更多: {movie_url}'}
# pp.pprint(params)
r = requests.post(url, headers=headers, params=params)
print(r.status_code)
