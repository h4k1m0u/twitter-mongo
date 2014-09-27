#!/usr/bin/env python

from flask import Flask, g, render_template, redirect, url_for
import pymongo
import tweepy

# mongodb config
DATABASE = 'twitter'
COLLECTION = 'tweets'

# twitter config
CKEY = 'dVtaSMi6bx0YMN9iNZtgqg'
CSECRET = 'DpsYN0vdUog7Kkw2pi630PuWB0MLkyPRlypf2Msbg'
ATOKEN = '1629980322-pN87FE7xf2cJl5buJF0F5QlduSfVPbKXLFGSHix'
ASECRET = 'fmWTVmtrIGhDc9ff87ikowQTfsC5y7Gk2wMj56IUsNQ'
USERNAMES = {
    'algeria': 'DilemAli',
    'world': 'YahooNews',
    'sport': 'YahooSports',
    'science': 'IFLScience'
}


# create app
app = Flask(__name__)
app.config.from_object(__name__)


@app.before_request
def before_request():
    """ Connect to mongodb database before each request,
        and initialize database & its collection.
    """
    try:
        # connect to mongodb server & create db and collection
        g.connection = pymongo.MongoClient()
        g.db = getattr(g.connection, app.config['DATABASE'])
        g.collection = getattr(g.db, app.config['COLLECTION'])
    except pymongo.errors.ConnectionFailure, e:
        print 'Could not connect to mongodb: %s' % e


@app.teardown_request
def teardown_request(exception):
    """ Disconnect from mongodb when app is closed or exception
    """
    db = getattr(g, 'db', None)
    if db is not None:
        g.connection.close()


@app.route('/')
def home():
    """ /algeria is the default home page to redirect to
    """
    return redirect(url_for('algeria'))


@app.route('/algeria')
def algeria():
    """ Get Twitter news in category algeria, from mongodb
    """
    tweets = g.collection.find({'category': 'algeria'})
    return render_template('tweets.html', **{
        'tweets': tweets,
        'title': 'Algeria',
        'username': '@AliDilem'
    })


@app.route('/world')
def world():
    """ Get Twitter news in category world, from mongodb
    """
    tweets = g.collection.find({'category': 'world'})
    return render_template('tweets.html', **{
        'tweets': tweets,
        'title': 'World',
        'username': '@YahooNews'
    })


@app.route('/sport')
def sport():
    """ Get Twitter news in category sport, from mongodb
    """
    tweets = g.collection.find({'category': 'sport'})
    return render_template('tweets.html', **{
        'tweets': tweets,
        'title': 'Sport',
        'username': '@YahooSports'
    })


@app.route('/science')
def science():
    """ Get Twitter news in category science, from mongodb
    """
    tweets = g.collection.find({'category': 'science'})
    return render_template('tweets.html', **{
        'tweets': tweets,
        'title': 'Science',
        'username': '@IFLScience'
    })


@app.route('/item/<id>')
def item(id):
    return render_template('tweets.html')


@app.route('/refresh/<category>')
def refresh(category=None):
    """ Refresh given category tweets from Twitter,
        And save retreived tweets on mongodb, then redirect to calling page
        Args:
            category(str): get tweets in this category
    """
    tweets = get_tweets(category)

    for tweet in tweets:
        data = {}
        data['id'] = tweet.id
        data['text'] = tweet.text
        data['category'] = category
        if 'media' in tweet.entities:
            data['url'] = tweet.entities['media'][0]['url']
            data['image'] = tweet.entities['media'][0]['media_url_https']

        g.collection.insert(data)

    return redirect(url_for(category))


def get_tweets(category):
    """ Get Twitter news in given category
        Args:
            category(str): get tweets in this category
        Returns:
            tweets(list): a list of tweets with their attributes
    """
    # oauth with twitter app
    auth = tweepy.OAuthHandler(app.config['CKEY'], app.config['CSECRET'])
    auth.set_access_token(app.config['ATOKEN'], app.config['ASECRET'])
    api = tweepy.API(auth)

    # get tweets
    tweets = tweepy.Cursor(
        api.user_timeline,
        id=app.config['USERNAMES'][category],
        include_entities=True
    ).items(10)

    return tweets


# run app
if __name__ == '__main__':
    app.run(debug=True)
