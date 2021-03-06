'''
@Description: This is Programming Assignment "3" for AIT 690: NLP class.This python program called tagger.py will take as input a training file containing part of speech tagged text, and a file containing text to be part of speech tagged. It will implement "most likely tag" baseline.


The program runs without any error and gives/predict tags for test file(2nd input) based on learned model using 1st input file as training data.

@ Problem Defination:Design and implement a Python program called tagger.py .For each word in the training data, assign it the POS tag that maximizes p(tag|word). Assume that any word found in the test data but not in training data (i.e. an unknown word) is an NN. which means, if a word for example 'you' appears as noun (NN ) 2 out of ten times and pronoun (PRP) 8 times in traing data then for "you" in test data assign it PRP tag as it mas more p(tag|word)


@Examples of program input and output :
Input:  tagger.py pos-train.txt pos-test.txt 
Output:  pos-test-with-tags.txt and test word + tag  to STDOUT

pos-train.txt          - Tagged training corpus with words and its tags
pos-test.txt 		    - Untagged test corpus 
pos-test-with-tags.txt - Tagged test corpus
pos-test-with-tags.txt will be used to evaluate accuracy and confusion matrix

@Algorithim:
		1)Argumnet Parsing for traing data and test data.
		2)Iterating through the files.
		3)convert train data to tuple of (word,tag) 
		4)The tag appearing most frequently for a given word is chosen and strored in a list which is considered as baseline model
		5)test data is converted to list of words to be tagged
		6)seven rules are defined to tag unknown words 
		   e.g
		   Rule 1: If  word is 'He'or'he' or'She'or'she'or'It'or'it'or'I'or'me'or'Me'or'You'or'you' tah=('PRP')
		   Rule 2 If word.endswith('s')   tag= ('NNS')
		   etc.
		7)The test words that are not found in the baseline model and dont fall into rules are given "NN" by default
		8)The above output is directed into pos-test-with-tags.txt for calculating accuracy.
		

@Authors: Sri Ram Sagar Kappagantula
          Harsimrat Kaur
          Ritika De
@Date: 17 Oct, 2018.

@Accuracy : Note:-The overall accuracy when rules are added is 85.09%
		 The overall accuracy when rules are not added and default tag is NN is 84.388%
'''

import argparse
import nltk
import copy, time, sys
from collections import Counter
from collections import defaultdict as ddict


##### MostLikelyTag

def train(tagged_train):
    _word_tags = dict()
    word_tag_counts = ddict(lambda: ddict(lambda: 0))
    for word, tag in tagged_train:
            word_tag_counts[word][tag] += 1

    # select the tag used most often for the word
    for word in word_tag_counts:
        tag_counts = word_tag_counts[word]
        tag = max(tag_counts, key=tag_counts.get)
        _word_tags[word] = tag
    return _word_tags

def predict(mylist):
    y=[]
    for word in mylist:
        if x.get(word):
            y.append(x.get(word))
                
        elif word[0] == word[0].upper():
            y.append('NN')
        elif word.istitle():
            y.append('NNP')
        elif word[0].isdigit():
            y.append('CD')
        elif word.endswith('s'):
            y.append('NNS')
        elif word.endswith('ing'):
            y.append('VBG')
        elif word.endswith('ed'):
            y.append('VBD') 
        elif word is 'He'or'he' or'She'or'she'or'It'or'it'or'I'or'me'or'Me'or'You'or'you':
            y.append('PRP')
        else:
            y.append('NN')
        
    return y

#########################################
def main():
	# get input: traing data->pos-train

	parser = argparse.ArgumentParser()
	parser.add_argument("file",type = str,nargs='+')                       #to take files from command prompt

	args = parser.parse_args()
	pos_train= open(args.file[0], 'rt', encoding="utf8") 			    #to open and read the training data.
	data_train = pos_train.read().split()

	#training data to to tuple [(word,tag)]

	tagged_train = [nltk.tag.str2tuple(t) for t in data_train]
	output=[(word,tag) for (word,tag) in tagged_train if tag !=None]      #remove elements with tag none  
	##########   # Test file begin

	test=open(args.file[1], 'rt', encoding="utf8")							#to open and read the test data.
	test_data=test.read().split()
	for i in range(len(test_data)):
		if '[' in test_data: test_data.remove('[')							#remove brackets from list of test data
		if ']' in test_data:test_data.remove(']') 														
		
	########################################	
		
	x=train(output)														#Get max likely tag for elements in training data
	
	test_tag = predict(test_data)

    for line in test_tag:

        sys.stdout.write("%s\n" %' '.join(line))										#print line by line to file


# main program

if __name__== '__main__':
    main()
                  
 #print("Total time : " + str(time.time() - start_time))