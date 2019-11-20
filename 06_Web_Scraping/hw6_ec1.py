# 507 Homework 6 Extra Credit 1
import requests
from bs4 import BeautifulSoup

#### Extra Credit 1 ####
print('\n*********** EXTRA CREDIT 1 ***********')
print('Top Headlines\n')

### Your Extra Credit 1 solution goes here
user_agent = {'User-agent': 'Mozilla/5.0'}
html = requests.get("https://www.michigandaily.com",headers=user_agent).text

soup = BeautifulSoup(html, 'html.parser')

sectors= ['News','Sports','Arts']

for s in sectors:
    print('Top 5 Headlines: '+s.lower())
    tags = soup.find('div',string=s).parent.parent.find_all(class_='views-field views-field-field-short-headline')
    cnt = 0
    for t in tags:
        cnt+=1
        if(cnt>5):
            break
        print(t.div.string)
    if s != 'Arts':
        print('')
