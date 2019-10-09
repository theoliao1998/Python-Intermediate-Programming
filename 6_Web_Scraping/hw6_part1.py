# 507 Homework 6 Part 1
import requests
from bs4 import BeautifulSoup

#### Part 1 ####
print('\n*********** PART 1 ***********')
print("-------Alt tags-------\n")

### Your Part 1 solution goes here

import sys

#usage should be python3 hw6_part1.py <url>

url = sys.argv[1]

html = requests.get(url).text

soup = BeautifulSoup(html, 'html.parser')

imgs = soup.find_all("img")

for img in imgs:
    alt = img.get('alt')
    if alt:
        print(alt)
    else:
        print("No alternative text provided!")
