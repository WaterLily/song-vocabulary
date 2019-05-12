# # pattern for decoding escaped unicode blocks
# test = r"\u00e2"
# decoded = bytes(test, "utf-8").decode("unicode-escape")

from constants import API_URL, STEM_DICT_PATH, UNIQUE_WORDS_PATH, SUBMITTED_WORDS_PATH, LOG_PATH
from hidden_constants import API_KEY
import requests
import json
import time


def load_unique_words():
    with open(UNIQUE_WORDS_PATH, "r") as in_file:
        unique_words = in_file.read().split("\n")[:-1]
    return set(unique_words)


def load_submitted_words():
    with open(SUBMITTED_WORDS_PATH, "r") as in_file:
        unique_words = in_file.read().split("\n")[:-1]
    return set(unique_words)


def save_submitted_word(word):
    with open(SUBMITTED_WORDS_PATH, "a") as out_file:
        out_file.write(word+"\n")


def load_dict():
    with open(STEM_DICT_PATH, "r") as f:
        translation_dict = json.load(f)
    return translation_dict


def save_dict(translation_dict):
    with open(STEM_DICT_PATH, "w") as f:
        json.dump(translation_dict, f)


def init_dict(word, stem):
    translation_dict = {word: stem}
    save_dict(translation_dict)


def init_submitted_words(word):
    with open(SUBMITTED_WORDS_PATH, "w") as f:
        f.write(word+"\n")


def load_remaining_words():
    unique_words = load_unique_words()
    submitted_words = load_submitted_words()
    return unique_words - submitted_words


def log_error(error_string):
    with open(LOG_PATH, "a") as log:
        log.write(error_string + "\n")
        log.write("*"*10 + "\n")


def query_stemmer(word):
    param_dict = {
        'api_key': API_KEY,
        'text': word,
    }
    res = requests.get(API_URL, params=param_dict)
    if res.status_code != 200:
        log_error("word: {}".format(word) + "\n" + "status_code: {}".format(res.status_code))
        raise AssertionError
    js = res.json()
    if js['success']:
        return js['result']
    else:
        print(js.get('errors', "No error message available"))
        raise RuntimeError


def process_batch(words, stem_dict):
    error_count = 0
    for word in words:
        save_submitted_word(word)
        try:
            stem = query_stemmer(word)
            error_count = 0
            if stem:
                stem_dict[word] = stem
        except (AssertionError, RuntimeError):
            error_count += 1
            if error_count > 5:
                log_error("Quit early.  Get some sleep.")
                break
        time.sleep(2)
