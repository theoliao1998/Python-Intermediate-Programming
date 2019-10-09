# 507 Homework 6 Part 2
import requests
from bs4 import BeautifulSoup


#### Part 2 ####
print('\n*********** PART 2 ***********')
print('Michigan Daily -- MOST READ\n')

### Your Part 2 solution goes here

user_agent = {'User-agent': 'Mozilla/5.0'}
html = requests.get("https://www.michigandaily.com",headers=user_agent).text

soup = BeautifulSoup(html, 'html.parser')

most_reads = soup.find(class_='view-id-most_read').find_all('li')

for li in most_reads:
    print(li.string)
