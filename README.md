Twitter-news
=============

Get `10 last` news in given `category` from Twitter.
Save them in a `MongoDB` collection.
And show them on a `Flask` mini-website.

**PS:**
User has to click on `Refresh` button to get latest News in current `category` from `Twitter` and save them on `MongoDb` server.
So tweets shown on website were saved on `MongoDB` before, in order to be loaded faster.

##Files:
* **twitter_news.py**: The main website.

##Prerequisite:
* **python**.
* **mongodb**.
* **flask**: Python micro web-framework.
* **pymongo**: MongoDb python client
* **tweepy**: Twitter python client (needs a twitter app).
