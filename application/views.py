from bs4 import BeautifulSoup
import urllib2
import json
import unicodedata
import logging
import sys
from collections import Counter
import datetime
import re
from pymongo import MongoClient
from application import app
from flask import render_template


stopwords = []
logging.getLogger().setLevel(logging.INFO)

# To get the HTML page contents


def get_page(url):
    page = urllib2.urlopen(url).read()
    return page


#@app.route('/stopwords',methods=['GET'])
def get_stopwords():
    global stopwords
    if stopwords:
        return stopwords
    else:
        for words in open('/Users/hhimanshu/code/p/python/newsanalysis/application/static/english', 'r').readlines():
            stopwords.append(words.strip())
        return stopwords
        # logging.info("stopwords appended to the list")

#'/Users/deeksha/desktop/application1/application/static/english'


# To get all the headlines for each city
def get_headlines_from_seedurl(seedurl):
    urlset = set()
    soup = BeautifulSoup(get_page(seedurl))
    for divtag in soup.findAll('h2'):
        try:
            url = divtag.find('a').get('href')
            urlset.add(url)
        except:
            logging.error("%s cannot be crawled" % (divtag))  # , str(sys.exc_info())))
            continue
    logging.info("crawl_urls: total urls %d" % (len(urlset)))
    return urlset


# To get the news data received from get_headlines_from_seedurl()
def get_news(seedurl):
    news = Counter()

    for eachheadline in get_headlines_from_seedurl(seedurl):
        logging.info('processing - %s' % (eachheadline,))
        soup = BeautifulSoup(get_page(eachheadline))
        for data in soup.findAll('p', class_="body"):
            try:
                wordlist = re.split(
                    '\W', (unicodedata.normalize('NFKD', data.find(text=True)).encode('ascii', 'ignore')).lower())
                news.update([words for words in wordlist if words not in get_stopwords()])
            except:
                logging.error('error normalizing: %s' % (data,))
                continue
    news = {key: value for key, value in news.iteritems() if value >= 9}
    return dict(news)


# To get the date,city and news for each city.
def get_final_data():
    seed = 'http://www.thehindu.com/news/cities/CITY/?union=citynews'
    cities = ['bangalore', 'delhi', 'hyderabad', 'chennai', 'coimbatore']
    city_news = {}
    summary = {}
    summary['date'] = datetime.date.today().strftime('%d-%m-%Y')
    for city in cities:
        url = seed.replace('CITY', city)
        logging.info("city is %s and date is %s" % (city, datetime.date.today()))
        city_news[city] = get_news(url)
        logging.info("getting the data for %s" % (summary))
    summary['data'] = city_news
    return summary

# establish database connection between mongoDb and MongoClient, create a database(news) and a collection(summary)


def database_connection():
    connection = MongoClient()
    db = connection.news
    collection = db.summary
    return collection

# save the data to "summary" collection


def save_to_database(summary):
    return database_connection().insert(summary)

# driver to start crawling data and saving to database


@app.route('/add', methods=["POST"])
def driver():
    summary = get_final_data()
    return save_to_database(summary)
    # return render_template('citynewssummary.html',data=summary)


# retrieve the data from the database
def retrieve_from_database(fordate):
    return database_connection().find_one(fordate, {'_id': 0})

# takes the date request from the front end and supply the fordate to retrieve_from_database(). Currently takes todays date


@app.route('/get_results', methods=["GET"])
def what_data():
    logging.info('get todays data')
    fordate = {"date": datetime.date.today().strftime('%d-%m-%Y')}
    logging.info("searching for dictionary %s" % (fordate, ))
    data = retrieve_from_database(fordate)
    return json.dumps(data)


@app.route('/', methods=["GET"])
def get_template():
    return render_template('main.html')
