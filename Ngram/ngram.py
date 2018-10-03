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
from random import choice

def get_text_corpus(files:list) -> str:
    " Returns a large string of all text files merged togather."
    raw_text = ['.']
    for fil in files:
        raw_text.append(open(fil, encoding='utf-8').read())
    raw_text = '.'.join(raw_text)  
    return re.sub('\n', ' ', raw_text) # Replace all newline with a space and create a long string.

def generate_start_word(cfd, n_gram):
    if n_gram == 1:
        return choice([word_type for word_type in types if not word_type in ('START-TAG', 'END-TAG')])    
    start_gram_tokens = [gram_token for gram_token in cfd.keys() if gram_token[0] == 'START-TAG']
    return(choice(start_gram_tokens))

def next_word(cfd, gram_token):
    return max(cfd[gram_token,].items(), key=lambda x: x[1])[0]

def generate_sentence(cfd, start_gram_token):
    sentence = [start_gram_token]
    _next = next_word(cfd, start_gram_token)
    sentence.append(_next)
    next_gram_token = start_gram_token[1:] + _next

    for i in range(500):
        _next = next_word(cfd, next_gram_token)
        sentence.append(_next)
        next_gram_token = next_gram_token[1:] + _next
        if _next == 'END-TAG':
            break
        elif _next in ('.', '?', '!'):
            break
    return sentence


if __name__ == "__main__":
    n_gram = int(sys.argv[1]) # Must be integer.
    sentence_count = int(sys.argv[2]) # Must be integer.
    files = sys.argv[3:] # List of filenames strings.
    max_trails = 100

    print("This program generates random {} sentences based on a {}-gram model.".format(sentence_count, n_gram))

    raw_text = get_text_corpus(files).lower()
    raw_text = '.' + raw_text
    sentences = nltk.sent_tokenize(raw_text)
    tagged_text = ''.join(['START-TAG' + sentence + 'END-TAG' for sentence in sentences])
    
    tokens = nltk.word_tokenize(tagged_text)
    types = list(set(tokens))
    print(types)

    print("Total number of Tokens (>1,000,000): {} and types {}".format(len(tokens), len(types)))
    
    from nltk.util import ngrams
    ngrams_container = ngrams(tokens, n_gram)
    cfd = nltk.ConditionalFreqDist((gram, distinct_word)
                                    for gram in ngrams_container 
                                    for distinct_word in types)
    print('1')
    set_start_clauses = {generate_start_word(cfd, n_gram)}
    print(set_start_clauses)
    print('2')
    trail_count = 0
    while len(set_start_clauses) <= (sentence_count-1):
        set_start_clauses.add(generate_start_word(cfd, n_gram))
        trail_count += 1
        if trail_count == max_trails:
            break
    
    for start_clause in set_start_clauses:
        print(generate_sentence(cfd, start_clause))