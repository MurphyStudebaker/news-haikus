#A python program to generate haikus from the Google News API
#Author: Murphy Studebaker

from newsapi import NewsApiClient
from hyphen import Hyphenator
import nltk
import config
import random

#API access setup
key = config.API_KEY
news_api = NewsApiClient(api_key=key)

#Language processing set up
hyphen = Hyphenator('en_US')

top_articles_data = []
keyword_data = []

line_1 = ["VB","NNP","NN","NNP","NN"]
line_2 = ["CC","NN", "CC", "JJ", "NN","VB"]
line_3 = ["NN", "IN", "NNP", "NN"]
pattern = [line_1, line_2, line_3]
position = 0;

def init():
    print ("~ ~ ~ ~ H A I K U ~ T H E ~ N E W S ~ ~ ~ ~\n")
    print ("1. Top Articles Today")
    print ("2. Top Articles for my Keyword")
    print ("3. Compare sources")
    selection = input("Select: ")
    print (selection)
    if (selection == "1"):
        top_articles_data = news_api.get_top_headlines(language='en', country='us')
        if (top_articles_data["status"] == "ok"):
            i = 5
            chosen = []
            while (i > 0):
                index = random.randint(0, 20)
                processedDesc = processArticle(top_articles_data, index, "description")
                processedTitle = processArticle(top_articles_data, index, "title")
                writeHaiku(pattern, processedDesc, processedTitle)
                i -= 1
        else:
            print ("Rain, ice, gloom, and fog \n because a fatal error \n occurred with data")
    elif (selection == "2"):
        keyword = input("Enter a news topic: ")
        keyword_data = news_api.get_everything(q=keyword)
        if (keyword_data["status"] == "ok" and keyword_data["totalResults"] > 3):
            print("Writing your haiku book . . .")
            i = 3
            while (i > 0):
                processedDesc = processArticle(keyword_data, i, "description")
                processedTitle = processArticle(keyword_data, i, "title")
                writeHaiku(pattern, processedDesc, processedTitle)
                i -= 1
        else:
            print ("Rain, ice, gloom, and fog \n because a fatal error \n occurred with data")
    elif (selection == "3"):
        print ("~ ~ ~ B B C ~ ~ ~")
        from_source("bbc-news")
        print ("~ ~ ~ B R E I T B A R T ~ ~ ~")
        from_source("breitbart-news")

    else:
        print ("My condolances, \n but your selection is wrong \n please attempt once more")

def processArticle(data, index, desired): #desired = description or title
    processed = []
    articles = data['articles']
    des = articles[index][desired]
    filter(str.isalnum, des)
    words = nltk.word_tokenize(des)
    for word in words:
        if (word.isalpha()):
            continue
        else:
            words.remove(word)
    tags = nltk.pos_tag(words)
    for word in tags:
        length = len(hyphen.syllables(word[0]))
        if (length == 0):
            length = 1 #adjust for bug
        entry = word + (length,)
        processed.append(entry)
    return processed

#for use with speech pattern, loops through until word has acceptable syllable count and matches part of speech
def write_line_wp(position, max_syllables, speech_pattern, processed_array): #selects each word
    remaining = max_syllables
    line = ""
    pattern_index = 0
    current = position;
    #current = random.randint(0,len(processed_array))
    while (remaining > 0):
        word = processed_array[current]
        if (word[2] <= max_syllables and word[1] in speech_pattern[pattern_index]):
            line += (word[0] + " ") #add string of word to the line
            remaining -= word[2] #subtract number of syllables from remaining syllables in line
            pattern_index += 1 #move to next desired part of speech
            word = (" ", " ", 10) #make it so the word will not be chosen again
        current += 1 #move to next word in article
        if (current >= len(processed_array)):
            current = 0 #reset to first word
            pattern_index += 1 #probably no matching word in article
        if (pattern_index >= len(speech_pattern)):
            line += "of " #default
            remaining -= 1
            pattern_index = 0
    return line

#for use without speech patterns, adds words in order according to syllable count
def write_line(position, max_syllables, processed_array):
    line = ""
    remaining = max_syllables
    current = position
    while (remaining > 0):
        if (current >= len(processed_array)): #loop back to start of array
            current = 0
        word = processed_array[current]
        if (word[2] <= remaining):
            line += (word[0] + " ")
            remaining -= word[2]
        current += 1

    return line

#prints three haikus from the desired source, according to source IDs listed on Google News API documentation
def from_source(source):
    i = 5
    while (i > 0):
        source_data = news_api.get_everything(sources=source)
        if (source_data["status"] == "ok" and source_data["totalResults"] > 3):
            print("Writing your haiku book . . .")
            i = 3
            while (i > 0):
                processedDesc = processArticle(source_data, i, "description")
                processedTitle = processArticle(source_data, i, "title")
                writeHaiku(pattern, processedDesc, processedTitle)
                i -= 1
        else:
            print ("Could not fetch articles from that source.")

#prints haiku by generating each line
def writeHaiku(pattern, desc, title):
    print ("\n~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n")
    print (write_line(0, 5, title))
    print (write_line(0, 7, desc))
    print (write_line(6, 5, desc))

init()
