import requests
from bs4 import BeautifulSoup
from itertools import chain
import re

# Build a request
url = "http://meucymru.co.uk/music/Songs/Caneuon.html"
headers = {'User-agent': 'jlbot 1.0'}
res = requests.get(url, headers=headers)
assert res.status_code == 200

soup = BeautifulSoup(res.content, 'lxml')

lyrics = []
for song in soup.findAll('h2'):
    curr_lyrics = []
    for sibling in song.next_siblings:
        if sibling.name == 'h2':
            break
        else:
            try:
                curr_lyrics.append(sibling.text.lower())
            except AttributeError as ae:
                curr_lyrics.append(sibling.lower())
    lyrics.append(" ".join(curr_lyrics))

# tokenize the lyrics into words
regex = r"(?<!\w['`’])([^\d\W]+)"
tokenized_lyrics = [re.findall(regex, song) for song in lyrics]

# build unique word list for optimized stemming
flat_word_list = set(chain.from_iterable(tokenized_lyrics))

num = 5
i = 0
print(len(flat_word_list))
for word in flat_word_list:
    if i < num:
        print(word)
    else:
        break
    i += 1
