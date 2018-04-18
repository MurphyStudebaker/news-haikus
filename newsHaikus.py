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

top_articles_data = []
keyword_data = []

line_1 = ["NNP","JJ","NN","NN","NN"]
line_2 = ["VB", "NNP", "RB", "NN","NN","NN","CC"]
line_3 = ["VB", "CC", "JJ", "VB","VB","VB"]
pattern = [line_1, line_2, line_3]

def init():
    print ("~ ~ ~ ~ H A I K U ~ T H E ~ N E W S ~ ~ ~ ~\n")
    print ("1. Top Articles Today")
    print ("2. Top Articles for my Keyword")
    selection = input("Select: ")
    print (selection)
    if (selection == "1"):
        top_articles_data = news_api.get_top_headlines(language='en', country='us')
        if (top_articles_data["status"] == "ok"):
            processed = processArticle(top_articles_data, 0)
            writeHaiku(pattern, processed)
        else:
            print ("Rain, ice, gloom, and fog \n because a fatal error \n occurred with data")
    elif (selection == "2"):
        keyword = input("Enter a news topic: ")
        keyword_data = news_api.get_top_headlines(q=keyword,
                                               language='en')
        if (keyword_data["status"] == "ok" and keyword_data["totalResults"] > 3):
            processed = processArticle(keyword_data, 0)
            writeHaiku(pattern, processed)
        else:
            print ("Rain, ice, gloom, and fog \n because a fatal error \n occurred with data")
    else:
        print ("My condolances, \n but your selection is wrong \n please attempt once more")

def processArticle(data, index):
    processed = []
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

def writeHaiku(pattern, processed):
    print ("\n~ ~ ~ ~ H A I K U ~ T H E ~ N E W S ~ ~ ~ ~\n")
    print (write_line(5, pattern[0], processed))
    print (write_line(7, pattern[1], processed))
    print (write_line(5, pattern[2], processed))

init()
