# entry level code and import text preprocess

from .text_preprocess import *

# General Feature Extraction


def extract_features(element):
    return {
        'word_count': word_count(element),
        'char_count': char_count(element),
        'avg_word_len': avg_word_len(element),
        'stop_words_count': stopwords_count(element),
        'hashtags_count': hashtags_count(element),
        'mentions_count': mentions_count(element),
        'numerics count': numerics_count(element),
        'upper_case_count': uppers_count(element)
    }

# Cleaning Text


def clean_text(element):
    element = to_lower_case(element)
    element = contraction_to_expansion(element)
    element = remove_emails(element)
    element = remove_urls(element)
    element = rm_html(element)
    element = rm_special_chars(element)
    element = lemmatize(element)
    return element
