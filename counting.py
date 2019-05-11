from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd

def get_counts(tokenized_lyric_list, stem_dict, save=True):
    cv = CountVectorizer(
        preprocessor=lambda x: [stem_dict[word] for word in x],
        tokenizer=lambda x: x,
    )
    count_data = cv.fit_transform(tokenized_lyric_list).toarray()
    counts = pd.DataFrame(count_data, columns=cv.get_feature_names())
    if save:
        counts.to_csv("./welsh_word_counts.csv")
    doc_freq = counts.astype(bool).sum().sort_values(ascending=False)
    if save:
        doc_freq.to_csv("./welsh_word_doc_frequencies.csv")
    return counts
