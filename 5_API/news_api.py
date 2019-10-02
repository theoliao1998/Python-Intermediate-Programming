
newsapi_key = ""

import requests
import json

# gets headlines for today's news


CACHE_FNAME = 'news_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}


def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_" + "_".join(res)

def make_request_using_cache(baseurl, params):
    
    unique_ident = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, params)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]
    

def fetch_top_headlines(category=None):
    baseurl = 'http://newsapi.org/v2/top-headlines'
    params={'country': 'us'}
    if category is not None:
        params['category'] = category
    params['apiKey'] = newsapi_key
    return make_request_using_cache(baseurl, params) #requests.get(baseurl, params).json()

def get_headlines(results_dict):
    results = results_dict['articles']
    headlines = []
    for r in results:
        headlines.append(r['title'])
    return headlines

science_list_json = fetch_top_headlines('science')
headlines = get_headlines(science_list_json)
for h in headlines:
    print(h)
