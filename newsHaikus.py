#A python program to generate haikus from the Google News API
#Author: Murphy Studebaker

from newsapi import NewsApiClient
from hyphen import Hyphenator
from nltk.tokenize import word_tokenize
import config

#API access setup
key = config.API_KEY
news_api = NewsApiClient(api_key=key)

#Language processing set up
hyphen = Hyphenator('en_US')

top_articles_data = news_api.get_top_headlines(language='en', country='us')
articlesFound = top_articles_data['totalResults']

keyword = input("Enter a news topic: ")
keyword_data = news_api.get_top_headlines(q=keyword,
                                       language='en')

#print syllables if data fetch was successful
if (keyword_data['status'] == 'ok'):
    headline = keyword_data['articles'][0]['title']
    words = word_tokenize(headline)

    for word in words:
        syllables = hyphen.syllables(word)
        for s in syllables:
            print (s)
else:
    print ("Error fetching data.")
