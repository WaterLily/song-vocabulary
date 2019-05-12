from scrape_lyrics import get_lyrics
from counting import get_counts
from stemming import load_remaining_words, process_batch, load_dict, save_dict, log_error
import time

INTER_BATCH_SLEEP_SECONDS = 5 * 60  # prev value: 5 * 60


def init():
    get_lyrics()


def chunk(a,n):
    stack = iter(a)
    while True:
        curr = 0
        curr_chunk = []
        while curr < n:
            try:
                curr_chunk.append(next(stack))
                curr += 1
            # if stack is exhausted, stop
            except StopIteration as e:
                if curr_chunk:
                    yield curr_chunk
                return
        yield curr_chunk


def batch_remaining_words(size):
    remaining = load_remaining_words()
    return chunk(remaining, size)


def build_stem_dict(test=False, batch_size=20, n_loops=5):
    curr_dict = load_dict()
    batches = batch_remaining_words(batch_size)
    batch_no = 0
    for word_batch in batches:
        start = time.time()
        start_dict_size = len(curr_dict)

        process_batch(word_batch, curr_dict)

        new_stems = len(curr_dict) - start_dict_size
        spent_seconds = time.time() - start
        if new_stems >= 0:
            print("finished batch {} in {} seconds".format(batch_no, spent_seconds))
            print("added {} entries to stem map".format(new_stems))
            save_dict(curr_dict)
        else:
            log_error('stem dictionary is corrupted')
            raise RuntimeError
        if spent_seconds < INTER_BATCH_SLEEP_SECONDS:
            time.sleep(INTER_BATCH_SLEEP_SECONDS - spent_seconds)
            batch_no += 1
        if test and batch_no >= n_loops:
            break
    return curr_dict


if __name__ == "__main__":
    lyrics, unique_words = get_lyrics()
    # print(len(lyrics))
    # print(lyrics[0])
    # print("*"*10)
    # print(unique_words[0])
    # print("...")
    # print(unique_words[-1])
    stem_dict = build_stem_dict()
    get_counts(lyrics, stem_dict)

