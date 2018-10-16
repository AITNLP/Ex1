import argparse
import nltk
import copy, time, sys
from collections import Counter
from collections import defaultdict as ddict

# get input

parser = argparse.ArgumentParser()
parser.add_argument("file",type = str,nargs='+')  #to take files from command prompt

args = parser.parse_args()
pos_train= open(args.file[0], 'rt', encoding="utf8") 			#to open and read the training data.
data_train = pos_train.read().split()

##############################################

"""remove ambiguous tags"""
  
################################ 

#training data to to tuple [(word,tag)]

tagged_train = [nltk.tag.str2tuple(t) for t in data_train]
output=[(word,tag) for (word,tag) in tagged_train if tag !=None]

##### MostLikelyTag


#tag_fd = nltk.FreqDist(tag for (word, tag) in tagged_train)
#tag_fd.most_common()

# count number of times a word is given each tag
def train(tagged_train):
    _word_tags = dict()
	word_tag_counts = ddict(lambda: ddict(lambda: 0))
	for words, tags in tagged_train:
		for word, tag in zip(words, tags):
			word_tag_counts[word][tag] += 1

	# select the tag used most often for the word
	for word in word_tag_counts:
		tag_counts = word_tag_counts[word]
		tag = max(tag_counts, key=tag_counts.get)
		_word_tags[word] = tag
    return _word_tags






##########   # Test file 

test=open(args.file[1], 'rt', encoding="utf8")									#to open and read the test data.
test_data=test.read().split()
test_data = list(filter(lambda x: x!= '[' , test_data)) 				
test_data = list(filter(lambda x: x!= ']', test_data))							#to remove phrasal boundaries
test_data= set(test_data) 														#to include the unique words and get rid of any duplicate.
mylist=list(test_data)															#to convert to list of words

##############################


########################################

import re

def tagger(dict_model):
    with open(args.file[1]) as f:
        lines = f.readlines()
        items = []
        for line in lines:
            if line.startswith('['):													#to identify phrasal boundaries

                newitems = re.search(r'\[ (.+) \]',line).group(1).split()

            else:																	#if no phrasal boundaries
                newitems = line.split()
            items.append(newitems)

    test_tag = []
    for line in items:
        tagged_line = []

        for item in line:

            tag = dict_model[item]

            tagged_line.append(item+'/'+tag)

        test_tag.append(tagged_line)

    return test_tag	
#########################################
def main():

    _model =  #have to write this -> type dict
	
    test_tag = tagger(_model)

    for line in test_tag:

        sys.stdout.write("%s\n" %' '.join(line))										#print line by line to file


# main program

if __name__== '__main__':
    main()
                  
 #print("Total time : " + str(time.time() - start_time))