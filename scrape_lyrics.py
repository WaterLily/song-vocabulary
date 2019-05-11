import requests
from bs4 import BeautifulSoup
from itertools import chain
import re
import csv

# parameters for scraping lyrics
URL = "http://meucymru.co.uk/music/Songs/Caneuon.html"
HEADERS = {'User-agent': 'jlbot 1.0'}
LYRIC_PATH = "./lyric_tokens.csv"
UNIQUE_WORD_LIST_PATH = "./unique_word_list.csv"

# scrape the lyrics
def get_lyrics(url=URL, headers=HEADERS, save=True):
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
    if save:
        with open(LYRIC_PATH, "w") as out_file:
            writer = csv.writer(out_file)
            writer.writerows(tokenized_lyrics)
        with open(UNIQUE_WORD_LIST_PATH, "w") as out_file:
            for word in flat_word_list:
                out_file.write(word+"\n")
    return tokenized_lyrics, flat_word_list

if __name__ == "__main__":
    get_lyrics()