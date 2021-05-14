import requests
from bs4 import BeautifulSoup

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
    #print(channel_num, channel_name, movie_title)
    result.append(f"{channel_num} {channel_name} {movie_title}")


# Line Notify
# ref. https://www.learncodewithmike.com/2020/06/python-line-notify.html
token = "your_token" # replace this with your token
url = "https://notify-api.line.me/api/notify"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/x-www-form-urlencoded"
}
params = {"message": "今晚九點\n" + "\n".join(result) + "\n" + movie_url}
r = requests.post(url, headers=headers, params=params)
print(r.status_code)

