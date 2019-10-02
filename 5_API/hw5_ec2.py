from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
# Uncomment following two lines after you install nltk
import nltk 
from nltk.corpus import stopwords

#nltk.download('stopwords')
#nltk.download('punkt')


#usage should be python3 hw5_ec2.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends


FNAME = 'tweet.json'

baseurl = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
params={'screen_name':username,'count':num_tweets}

def getTweets(baseurl,params):
    res = json.loads(requests.get(baseurl,params,auth=auth).text)
    if __name__ == "__main__":  # when imported for extra, we are not asked to write
        dumped_res = json.dumps(res, indent=2)
        fw = open(FNAME,"w")
        fw.write(dumped_res)
        fw.close()
    return res

def analyzeTweets(res):
    token = []
    for tweet in res:
        token += nltk.word_tokenize(tweet['text'])

    token_filtered = [t for t in token if ((t[0] >= 'a' and t[0] <= 'z') or (t[0] >= 'A' and t[0] <= 'Z')) and (t not in stopwords.words("english")) and (t not in ['http','https','RT'])]
    fdist = nltk.FreqDist(token_filtered)
    print("USER: "+username)
    print("TWEETS ANALYZED: "+num_tweets)
    words = [pair[0]+"("+repr(pair[1])+")" for pair in fdist.most_common(5)]
    print("5 MOST FREQUENT WORDS: " +" ".join(words))

#Code for Caching

CACHE_FNAME = 'tweets_cache2.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}


def make_request_using_cache(baseurl, params):
    
    id_new = json.loads(requests.get(baseurl,{'screen_name':username,'count':1},auth=auth).text)[0]["id_str"]
    unique_ident = username +"-" + id_new
    
    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Fetching cached data...")
        res = CACHE_DICTION[unique_ident]
        dumped_res = json.dumps(res, indent=2)
        fw = open(FNAME,"w")
        fw.write(dumped_res)
        fw.close()
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        # Make the request and cache the new data
        res = getTweets(baseurl, params)
        CACHE_DICTION[unique_ident] = res
        dumped_json_cache = json.dumps(CACHE_DICTION,indent=2)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]



if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
    
    res = make_request_using_cache(baseurl,params)
    analyzeTweets(res)

