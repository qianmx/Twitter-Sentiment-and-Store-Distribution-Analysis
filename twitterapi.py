import sys
import tweepy
import string
import re
from textblob import TextBlob
from collections import defaultdict
import numpy as np
import pandas as pd


KEY = sys.argv[1]
SECRET = sys.argv[2]


auth = tweepy.AppAuthHandler(KEY, SECRET)
api = tweepy.API(auth, wait_on_rate_limit= True, wait_on_rate_limit_notify= True)

states_dir = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


def cleanse(text):
    """
    Removes punctuation special characters and links.
    """
    text = text.lower()
    nonalpha = re.compile('[' + string.punctuation + '0-9\\r\\t\\n' + ']')
    no_links = re.sub('http[\S]+|www[\S]+', ' ', text)
    text = re.sub(nonalpha, ' ', no_links)
    text = re.sub('[ ]+', ' ', text)

    return text


def get_tweets(search_term, max_tweets):
    calls = 0
    tweets = api.search(q=search_term, lang='en', count=100, geocode="38.134557,-96.328125,2508km")
    calls += 1
    tweet_ids = [tweet.id for tweet in tweets]
    state_dict,tweet_ids, count = tweet_state_sentiment(tweet_ids, tweets)
    min_id = min(tweet_ids)

    while count < max_tweets:
        tweets = api.search(q=search_term, lang='en', count=100, max_id=min_id-1, geocode="38.134557,-96.328125,2508km")
        calls += 1
        # Grabbing Information from tweets
        state_dict, tweet_ids, count = tweet_state_sentiment(tweet_ids, tweets, state_dict, count)
        print 'Tweets: %d, Tweet IDs: %d, Queries: %d' % (count, len(tweet_ids), calls)
        min_id = min(tweet_ids)

    return state_dict


def tweet_state_sentiment(tweet_ids, tweets, state_dict = defaultdict(list), count=0):
    for tweet in tweets:
        if tweet.id not in tweet_ids:
            tweet_ids.append(tweet.id)
            search_state = re.search(", [A-Z]{2,}", tweet.user.location.strip().encode('ascii', 'ignore'))
            print tweet.user.location.strip()
            if search_state:
                State = search_state.group(0)[2:]
                if State in states_dir:
                    text = cleanse(tweet.text.strip().encode('ascii', 'ignore'))
                    sentiment = TextBlob(text).sentiment.polarity
                    state_dict[State].append(sentiment)
                    count += 1
    return state_dict, tweet_ids, count


if __name__ == '__main__':
    dict = get_tweets('nike', 1000)
    sentiment_score = {i: np.mean(dict[i]) for i in dict}
    df = pd.DataFrame(sentiment_score.items(), columns=['States', 'Sentiment'])
    df.to_csv('sentimentscore.csv')