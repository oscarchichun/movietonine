import requests
from bs4 import BeautifulSoup

# cron job for e.g. 07:00 every Sat. and Sun.
# 0 7 * * 0,6 /Library/Frameworks/Python.framework/Versions/3.9/bin/python3 /Users/oscarchao/project/python/get_movie_list/get_movie_list.py

# 開眼電影網 - 西片
movie_url = 'http://tv.atmovies.com.tw/tv/attv.cfm?action=todaytime'
r = requests.get(movie_url)
r.encoding = 'utf-8'

soup = BeautifulSoup(r.text, 'lxml')

result = []
tags = soup.find_all("td", string="21:00")
for tag2100 in tags:
    content_tag = tag2100.find_next_sibling("td")
    movie_title = content_tag.find("font", class_="at11").string
    if content_tag.find("font", color="#606060", string="首 "):
        movie_title += "(首播)"

    channel_tag = tag2100.find_parent("table", class_="at9").find_previous_sibling("a")
    channel_name = channel_tag.string
    channel_num = channel_tag.find_previous_sibling("a").attrs['name']
    #print(channel_num, channel_name, movie_title)
    result.append(f"{channel_num} {channel_name} {movie_title}")


# Line Notify
# ref. https://www.learncodewithmike.com/2020/06/python-line-notify.html

#  === replace this with your token === #
token = "your_token"

url = "https://notify-api.line.me/api/notify"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/x-www-form-urlencoded"
}
params = {"message": "今晚九點\n" + "\n".join(result) + "\n" + movie_url}
#print(params)
r = requests.post(url, headers=headers, params=params)
print(r.status_code)

