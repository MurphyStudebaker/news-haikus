# news-haikus
This is a project that uses the Google News API and linguistic processing libraries
to turn news headlines and articles into haikus that capture the media in a new light.

# Dependencies
The following libraries must be installed before running:
PyHyphen Library
(pip install phyhyphen)
Natural Language Toolkit
(pip install -U nltk)

A Google News API key is needed to run this program. It can be obtained at https://newsapi.org/ and
added to the config.py file, or replaced on line 11 of newsHaikus.py.

When the program is run, it will print a menu with three selection options. The first
prints a haiku book from the day's top news stories. The second prompts the user for a
keyword (Note that only extremely relevant keywords will produce results) before printing
a haiku book of articles with that keyword. The third option prints books from
different news sources that can be specified in the code according to the API source tags.

This program must run on a computer connected to the internet in order to work. 
