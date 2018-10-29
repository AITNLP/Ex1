import sys
import nltk
import string
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
from copy import copy
from collections import defaultdict

import logging
logger = logging.getLogger('WSD')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

def process_children(element):
    '''
    Return concatinated text string from xml children elemnets.
    '''
    text = ''
    for child in element.getchildren():
        try:
            text = text + ' ' + child.text
        except TypeError:
            pass
    return text

def get_context_list_train(xmlobject):
    '''
    Converts training data XML element tree to a python list of dictionaries to use as data frame.
    '''
    data = []
    dict_item = {}
    iterator = xmlobject.iter()
    for element in iterator:
        if element.tag == 'context':
            dict_item['context'] = process_children(element)
            data.append(copy(dict_item))
            dict_item = {}
            continue
        elif element.tag == 'answer':
            dict_item['senseid'] = element.attrib.get('senseid')
            dict_item['element'] = ET.tostring(element).decode("utf-8").strip('\n')
            continue
    return data

def get_dataframe_train_data(train_file):
    '''
    Returns dataframe for training data.
    '''
    train_data = ET.parse(train_file)
    train_data = get_context_list_train(train_data)
    return pd.DataFrame(train_data, columns=["element", 'senseid', 'context'])

def get_context_list_test(xmlobject):
    '''
    Converts test data XML element tree to a python list of dictionaries to use as data frame.
    '''
    data = []
    data_item = {}
    iterator = xmlobject.iter()
    for element in iterator:
        if element.tag == 'instance':
            data_item['id'] = element.attrib.get('id')
            data_item['context'] = process_children(element.getchildren()[0])
            data.append(copy(data_item))
    return data

def get_dataframe_test_data(test_file):
    '''
    Returns dataframe for test data.
    '''
    test_data = ET.parse(test_file)
    test_data = get_context_list_test(test_data)
    return pd.DataFrame(test_data, columns=['id', 'context'])

def clean_data(df, column_name):
    '''
    Removes punctuations, stopwords and create word tokens per sense instance.
    '''
    stopwords = nltk.corpus.stopwords.words('english')
    remove_punct = lambda text: ''.join((char for char in text if char not in string.punctuation))
    remove_stopwords = lambda sentence: [word for word in sentence.lower().split() if word not in stopwords]
    unpunct_array = df[column_name].apply(remove_punct)
    df['word_tokens'] = unpunct_array.apply(remove_stopwords)
    return df

def get_tagged_features_freq(df, column_name):
    '''
    Generate feature vectors for phone and product senses.
    '''
    df['pos_tag'] = df[column_name].apply(nltk.pos_tag)
    all_feature_phone = defaultdict(lambda: 0)
    all_feature_product = defaultdict(lambda: 0)
    for pos_set in df[df['senseid'] == 'phone']['pos_tag']:
        for word_tag in pos_set:
            all_feature_phone[word_tag] = all_feature_phone[word_tag] + 1
    for pos_set in df[df['senseid'] == 'product']['pos_tag']:
        for word_tag in pos_set:
            all_feature_product[word_tag] = all_feature_product[word_tag] + 1
    return all_feature_phone, all_feature_product

def score(pos_set, feature_set):
    '''
    Score parts of speech tagged token set with feature_set (i.e. Can be sense feature set for phone sense or product sense)
    '''
    score_ = 0
    for word_tag in pos_set:
        score_ = score_ + feature_set[word_tag]
    return score_
    
if __name__ == '__main__':
    global logger
    
    # STEP-1: Get inputs for system console
    train_file = sys.argv[1]
    test_file = sys.argv[2]
    output_file = sys.argv[3]
    
    hdlr = logging.FileHandler('/var/tmp/myapp.log')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.WARNING)

    # STEP-2: load training data to pandas dataframe.
    train_df = get_dataframe_train_data(train_file)
    train_df['tokens'] = train_df['context'].apply(nltk.word_tokenize)

    # STEP-3: Clean training data.
    train_df = clean_data(train_df, 'context')

    # STEP-4: Generate feature vectors for phone and product.
    freq_features_phone, freq_features_product = get_tagged_features_freq(train_df, 'word_tokens')

    # STEP-5: Get count of phoe and product sense count.
    phone_freq = train_df[train_df['senseid'] == 'phone'].shape[0]
    product_freq = train_df[train_df['senseid'] == 'product'].shape[0]

    # STEP-6: load test data to pandas dataframe.
    test_df = get_dataframe_test_data(test_file)

    # STEP-7: clean test data.
    test_df = clean_data(test_df, 'context')

    # STEP-8: POS tag test data.
    test_df['pos_tag'] = test_df['word_tokens'].apply(nltk.pos_tag)

    # STEP-9: score test data cross phone feature vector.
    test_df['phone_score'] = test_df['pos_tag'].apply(score, args=(freq_features_phone,))

    # STEP-10: score test data cross product feature vector.
    test_df['product_score'] = test_df['pos_tag'].apply(score, args=(freq_features_product,))

    # STEP-11: score test data cross product feature vector.
    test_df['sense'] = np.where(test_df['phone_score'] > test_df['product_score'], 'phone',
                       np.where(test_df['phone_score'] < test_df['product_score'], 'product', 'phone'))
    
    # STEP-12: prediction to sysout
    for id_, sense in zip(test_df['id'], test_df['sense']):
        print(f'<answer instance="{id_}" senseid="{sense}"/>')

# python decision-list.py PA4/line-train.xml PA4/line-test.xml my-decision-list.txt
