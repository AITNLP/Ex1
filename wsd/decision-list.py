import sys
import nltk
import pandas as pd
import xml.etree.ElementTree as ET
from copy import copy
from sklearn.feature_extraction.text import CountVectorizer

def process_children(element):
    text = ''
    for child in element.getchildren():
        try:
            text = text + ' ' + child.text
        except TypeError:
            pass
    return text

def get_context_list_train(xmlobject):
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
    train_data = ET.parse(train_file)
    train_data = get_context_list_train(train_data)
    return pd.DataFrame(train_data, columns=["element", 'senseid', 'context'])

def get_context_list_test(xmlobject):
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
    test_data = ET.parse(test_file)
    test_data = get_context_list_test(test_data)
    return pd.DataFrame(test_data, columns=['id', 'context'])

def clean_data(df, column_name):
    stopwords = nltk.corpus.stopwords.words('english')
    remove_punct = lambda text: ''.join((char for char in text if char not in string.punctuation))
    remove_stopwords = lambda token_list: [word for word in token_list if word not in stopwords]
    df['unpunct'] = df[column_name].apply(remove_punct)
    df['word_tokens'] = df['unpunt'].apply(remove_stopwords)
    df.drop(columns=['unpunct',])
    return df

def pos_tag(df, column_name):
    df['pos_tag'] = df[column_name].apply(nltk.pos_tag)
    return df

if __name__ == '__main__':
    train_file = sys.argv[1]
    test_file = sys.argv[2]
    output_file = sys.argv[3]
    train_df = get_dataframe_train_data(train_file)
    test_df = get_dataframe_test_data(test_file)
    train_df['tokens'] = train_df['context'].apply(nltk.word_tokenize)
    train_df = clean_data(train_df, 'context')
    train_df = pos_tag(train_df, 'word_tokens')
