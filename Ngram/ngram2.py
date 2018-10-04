'''
@Description:
@Authors: Sri Ram Sagar Kappagantula
          Harsimrat Kaur
          Ritika De
@Date: 1st Oct, 2018.
'''

import sys
import operator
from nltk import sent_tokenize, word_tokenize
import re
from collections import Counter
from collections import defaultdict
from random import choice

def get_text_corpus(files):
    """ Returns a large string of all text files merged togather."""
    raw_text = []
    for fil in files:
        raw_text.append(open(fil, encoding='utf-8').read())
    raw_text = ' '.join(raw_text)
    return re.sub('\n', ' ', raw_text) # Replace all newline with a space and create a long string.

def get_types(tokens):
    """ Returns all the types of text in-order in a list."""
    seen = set()
    seen_add = seen.add
    return [x for x in tokens if not (x in seen or seen_add(x))]

def generate_start_word(cdf, n_gram):
    """ Generate start tagged words and randomly choose one word out of them"""
    if n_gram == 1:
        return choice([word_type for word_type in types if not word_type in ('START-TAG', 'END-TAG')])
    start_gram_tokens = [gram_token for gram_token in cdf.keys() if gram_token[0] == 'START-TAG']
    return(choice(start_gram_tokens))

def check_next_exists(cfd, gram_token):
    """ Check existance of n-gram token in probability table from n-gram and unigram"""
    return True if cfd[gram_token] else False

def next_word(cfd, gram_token):
    """ Genearate next work at random to choose from the probability n-garam and unigram table."""
    new_gram = gram_token[1:]
    words_ = []
    for word in cfd[gram_token].keys():
        if check_next_exists(cfd, new_gram + (word,)):
            words_.append(word)
    if words_:
        return choice(words_)
    return 'END-TAG'

def generate_sentence(cfd, start_gram_token, types):
    sentence = [*start_gram_token] if isinstance(start_gram_token, tuple) else [start_gram_token]
    _next = next_word(cfd, start_gram_token)

    next_gram_token = (_next,) if isinstance(start_gram_token, str) else start_gram_token[1:] + (_next,)
    for i in range(10):
        _next = next_word(cfd, next_gram_token)
        sentence.append(_next)
        next_gram_token = next_gram_token[1:] + (_next,)
        if _next == 'END-TAG':
            break
        elif _next in ('.', '?', '!'):
            break
    return ' '.join([word for word in sentence if word not in ['START-TAG', 'END-TAG']])

if __name__ == "__main__":
    n_gram = int(sys.argv[1]) # Must be integer.
    sentence_count = int(sys.argv[2]) # Must be integer.
    files = sys.argv[3:] # List of filenames strings.
    max_trails = 10000

    print("This program generates random {} sentences based on a {}-gram model.".format(sentence_count, n_gram))
    raw_text = get_text_corpus(files).lower()
    sentences = sent_tokenize(raw_text)
    tagged_text = ''.join([' START-TAG ' + sentence + ' END-TAG ' for sentence in sentences])
    
    tokens = word_tokenize(tagged_text)
    freq_words = Counter(tokens) #dict of counts
    total_words = float(sum(iter(freq_words.values())))
    types = get_types(tokens)

    print("Total number of Tokens (>1,000,000): {} and types {}".format(len(tokens), len(types)))
    
    from nltk.util import ngrams
    print('Creating ngrams container!!!')
    n_grams_container = ngrams(tokens, n_gram) # should I calculate n-1 gram or for n-gram input???
    freq_n_gram = Counter(n_grams_container)
    total_n_grams = float(sum(iter(freq_n_gram.values())))
    p_next_lookup_table = defaultdict(dict)
    print("Creating propability tables.")
    for ngram, f_ngram in freq_n_gram.items():
        for _next, f_word in freq_words.items():
            p_next_lookup_table[ngram].update({_next : f_word/f_ngram})
    print("Finished probability table")

    set_start_clauses = {generate_start_word(p_next_lookup_table, n_gram)}

    if sentence_count > len(set_start_clauses):
        set_start_clauses = list(set_start_clauses)
        len_set_clauses = len(set_start_clauses)
        for i in range(sentence_count - len_set_clauses):
              set_start_clauses.append(choice(set_start_clauses))
        for start_clause in set_start_clauses:
            print(generate_sentence(p_next_lookup_table, start_clause, types))
    elif sentence_count == len(set_start_clauses):
        for start_clause in set_start_clauses:
            print(generate_sentence(p_next_lookup_table, start_clause, types))
    else:
        for start_clause in tuple(set_start_clauses)[:sentence_count]:
            print(generate_sentence(p_next_lookup_table, start_clause, types))
