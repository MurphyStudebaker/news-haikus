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
#print syllables if data fetch was successful
def processArticle(data, index):
    processed = []
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
        return processed

    else:
        print ("Error fetching data.")

def write_line(max_syllables, speech_pattern, processed_array): #selects each word
    remaining = max_syllables
    line = ""
    pattern_index = 0
    current = 0
    while (remaining > 0):
        word = processed_array[current]
        if (word[2] <= max_syllables and word[1] == speech_pattern[pattern_index]):
            line += (word[0] + " ") #add string of word to the line
            remaining -= word[2] #subtract number of syllables from remaining syllables in line
            pattern_index += 1 #move to next desired part of speech
        current += 1 #move to next word in article
        if (current >= len(processed_array)):
            current = 0 #reset to first word
            pattern_index += 1 #probably no matching word in article
        if (pattern_index >= len(speech_pattern)):
            line += "of " #default
            remaining -= 1
            pattern_index = 0
    return line

line_1 = ["NNP","JJ","NN","NN","NN"]
line_2 = ["VB", "NNP", "RB", "NN","NN","NN","CC"]
line_3 = ["VB", "CC", "JJ", "VB","VB","VB"]
processed = processArticle(top_articles_data, 6)
print (top_articles_data["articles"][6]["description"])
print ("\n~ ~ ~ ~ H A I K U ~ T H E ~ N E W S ~ ~ ~ ~\n")
print (write_line(5, line_1, processed))
print (write_line(7, line_2, processed))
print (write_line(5, line_3, processed))
