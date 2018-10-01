'''
@Description:
@Authors: Sri Ram Sagar Kappagantula
          Harsimrat Kaur
          Ritika De
@Date: 1st Oct, 2018.
'''
import sys
import nltk
import re
from collections import Counter

def get_text_corpus(files:list) -> str:
    " Returns a large string of all text files merged togather."
    raw_text = []
    for fil in files:
        raw_text.append(open(fil.read()))
    raw_text = '.'.join(raw_text)  
    return re.sub('\n', ' ', raw_text) # Replace all newline with a space and create a long string.
    
def tag_sentence_end(text:str) -> str:
    " Return the end tagged raw string."
    mod_text = re.sub( r'\.', '.<END>', text)
    mod_text = re.sub( r'\?', '?<END>', mod_text)
    mod_text = re.sub( r'!', '!<END>', mod_text)
    return mod_text

if __name__ == "__main__":
    n_gram = sys.argv[1] # Must be integer.
    sentence_count = sys.argv[2] # Must be integer.
    files = sys.argv[3:] # List of filenames strings.

    print("This program generates random {} sentences based on a {}-gram model.".format(sentence_count, n_gram))

    raw_text = get_text_corpus(files).lower()
    raw_text = tag_sentence_end(raw_text)

    tokens = nltk.word_tokenize(raw_text)

    print("Total number of Tokens (>1,000,000): {}".format(len(tokens)))
    token_hist = Counter(tokens)
    types = list(token_hist.keys())

    # TODO adding start.
    # NEED condition when we can add start and end tags.
    
    from nltk.util import ngrams
    ngrams_container = ngrams(tokens, n_gram)
