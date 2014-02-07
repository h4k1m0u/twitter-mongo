#!/usr/bin/python
import tweepy
import pymongo

# connect to mongo & init collection
try:
    conn = pymongo.MongoClient()
    print 'connected successfully to MongoDb'
except pymongo.errors.ConnectionFailure, e:
    print 'could not connect to MongoDb %s' % e

db = conn.twitter
tweets_collection = db.tweets

# config twitter app
ckey = ''
csecret = ''
atoken = ''
asecret = ''

# oauth to twitter app
auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)

# get tweets & save them to mongodb
tweets = tweepy.Cursor(
    api.search,
    q='#Algerie'
).items(10)

for tweet in tweets:
    data ={}
    data['id'] = tweet.id
    data['created_at'] = tweet.created_at
    data['favorite_count'] = tweet.favorite_count
    data['user'] = tweet.user.name
    data['geo'] = tweet.geo
    data['lang'] = tweet.lang
    data['source'] = tweet.source
    data['source_url'] = tweet.source_url
    data['text'] = tweet.text

    # save to mongodb collection
    tweets_collection.insert(data)
