# 507 Homework 7 Part 1
import requests
import json
from bs4 import BeautifulSoup

from datetime import date # used for cache (using cache with the same date)

#### Your Part 1 solution goes here ####
def get_umsi_data(page):
    #### Implement your function here ####
    page_url = catalog_url_base + "&page=" + repr(page)
    page_text = make_request_using_cache(page_url,header)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    if not page_soup.find(class_="field-items"):
        return None
    
    details = page_soup.find_all(class_="field-name-contact-details")
    details = [d.div.div.a['href'] for d in details]
    res = {}
    for href in details:
        url = baseurl + href
        
        soup = BeautifulSoup(make_request_using_cache(url,header), 'html.parser')
        email = soup.find(class_='field-type-email').contents[1].div.a.string
        name = soup.find(class_='field-name-title').div.div.h2.string
        title = soup.find(class_='field-name-field-person-titles').div.div.string
        res[email] = {"name":name,"title":title}
    
    return res


def get_unique_key(url):
    return url 

def make_request_using_cache(url, header):
    unique_ident = get_unique_key(url) +" " +str(date.today())

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url, headers=header)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]


#### Execute funciton, get_umsi_data, here ####

CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

baseurl = 'https://www.si.umich.edu'
catalog_url_base = baseurl + '/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All'
header = {'User-Agent': 'SI_CLASS'}
page_num = 0
data = {}
while True:
    new_data = get_umsi_data(page_num)
    if not new_data:
        break
    
    data.update(new_data)
    page_num += 1

#### Write out file here #####
with open('directory_dict.json', 'w') as outfile:
    json.dump(data, outfile, indent=0)