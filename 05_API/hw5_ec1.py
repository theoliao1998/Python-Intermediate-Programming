# This program compares the most frequent words of 
# user umsi and Umich based on their recent 25 tweets

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

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

user1 = 'umsi'
user2 = 'UMich'
count = '25'

baseurl = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
params1={'screen_name':user1,'count':count}
params2={'screen_name':user2,'count':count}

def analyzeTweets(res):
    token = []
    for tweet in res:
        token += nltk.word_tokenize(tweet['text'])

    token_filtered = [t for t in token if ((t[0] >= 'a' and t[0] <= 'z') or (t[0] >= 'A' and t[0] <= 'Z')) and (t not in stopwords.words("english")) and (t not in ['http','https','RT'])]
    return dict(nltk.FreqDist(token_filtered))

if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
    
    res1 = json.loads(requests.get(baseurl,params1,auth=auth).text)
    res2 = json.loads(requests.get(baseurl,params2,auth=auth).text)
    
    token1 = analyzeTweets(res1)
    token2 = analyzeTweets(res2)
    
    shared = {}
    unique1 = {}
    unique2 = {}
    
    for k in set(token1.keys()).union(set(token2.keys())):
        if k in token1 and k in token2:
            shared[k] = token1[k]+token2[k]
        elif k in token1:
            unique1[k] = token1[k]
        else:
            unique2[k] = token2[k]
    
    print("5 most frequent different(unique) words of "+ user1+" are:")
    words = [pair[0]+"("+repr(pair[1])+")" for pair in nltk.FreqDist(unique1).most_common(5)]
    print(" ".join(words))
    
    print("5 most frequent different(unique) words of "+ user2+" are:")
    words = [pair[0]+"("+repr(pair[1])+")" for pair in nltk.FreqDist(unique2).most_common(5)]
    print(" ".join(words))
    
    print("5 most frequent common words (shared by both) are:")
    words = [pair[0]+"("+repr(pair[1])+")" for pair in nltk.FreqDist(shared).most_common(5)]
    print(" ".join(words))   
    
