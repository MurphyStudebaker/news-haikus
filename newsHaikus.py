#A python program to generate haikus from the Google News API
#Author: Murphy Studebaker

from newsapi import NewsApiClient
import config

#API access setup
key = config.API_KEY
news_api = NewsApiClient(api_key=key)

top_articles_data = news_api.get_top_headlines(language='en', country='us')
articlesFound = top_articles_data['totalResults']

for article in top_articles_data['articles']:
    print ("ARTICLE: ")
    print (article['title'])
