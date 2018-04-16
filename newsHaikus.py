#A python program to generate haikus from the Google News API
#Author: Murphy Studebaker

from newsapi import NewsApiClient
from hyphen import Hyphenator
import nltk
import config

#API access setup
key = config.API_KEY
news_api = NewsApiClient(api_key=key)

#Language processing set up
hyphen = Hyphenator('en_US')

top_articles_data = news_api.get_top_headlines(language='en', country='us')
articlesFound = top_articles_data['totalResults']

#keyword = input("Enter a news topic: ")
#keyword_data = news_api.get_top_headlines(q=keyword,
#                                       language='en')
processed = []
#print syllables if data fetch was successful
def process(data, index):
    if (data['status'] == 'ok'):
        articles = data['articles']
        description = articles[index]['description']
        words = nltk.word_tokenize(description)
        tags = nltk.pos_tag(words)
        for word in tags:
            length = len(hyphen.syllables(word[0]))
            if (length == 0):
                length = 1 #adjust for bug
            entry = word + (length,)
            processed.append(entry)

    else:
        print ("Error fetching data.")

def select(syllableCount):
    syllablesRemaining = syllableCount
    wordIndex = 0
    line = ""
    while (syllablesRemaining > 0):
        current = processed[wordIndex]
        #print (current[0])
        if (syllablesRemaining >= current[2]): #number of syllables in current word
            line += (current[0] + " ")
            #print ("selected!")
            syllablesRemaining -= current[2] #subtract amount of syllables added
        wordIndex += 1
    #continue looping through words until line is filled
    return line

process(top_articles_data, 10)
print (select(5))
