# 507 Homework 7 Part 1
import requests
import json
from bs4 import BeautifulSoup

def get_trending_data():
    main_url = baseurl + "/news/"
    main_text = requests.get(main_url, headers=header).text
    main_soup = BeautifulSoup(main_text, 'html.parser')
    links = main_soup.find_all(lambda tag:tag.name == "a" and tag.has_attr('data-track-label') and 'trending' in tag["data-track-label"])
    res = []
    for a in links:
        page_url = baseurl + a['href']
        page_text = requests.get(page_url, headers=header).text
        page_soup = BeautifulSoup(page_text, 'html.parser')

        title = page_soup.find(class_='asset-headline').string.strip()
        print(title)

        author = page_soup.find(class_='asset-metabar-author')
        author = author.a.string.strip() if author.a else author.string.strip()

        published_time = page_soup.find(class_='asset-metabar-time')
        if published_time.span:
            published_time = str(published_time)
            published_time = published_time[published_time.find('Published ')+len('Published '):published_time.find(' | ')].strip()
        else:
            published_time = published_time.string.replace("Published ","").strip()
            
        res.append({"title":title,"byline":author,"publication_time":published_time})
    return res

#### Execute funcitons here ####
baseurl = 'https://www.freep.com'
header = {'User-agent': 'Mozilla/5.0'}

data = get_trending_data()

#### Write out file here #####
with open('freep.json', 'w') as outfile:
    json.dump(data, outfile, indent=0)