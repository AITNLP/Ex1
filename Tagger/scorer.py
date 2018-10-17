"""
@Program Name: "scorer.py" 
@Problem: Once tagger.py has tagged the test corpus, we need to find the accuracy of our tagger. The accuracy 
            of the tagged test corpus is compared with a gold standard key which is manually tagged version of the  
			 test corpus. scorer.py compares both the files and generates the confusion matrix along with accuracy.
 
@Examples of program input and output :
			Input: >python scorer.py pos-tag.txt pos-test-key.txt report.txt
			Output:reort.txt
			
			report.txt can have any name and file by that name will be generated that will habe confusion matrix and Accuracy printed in it
			
@Description:  The program is run from the command line as follows:
      python scorer.py pos-test-with-tags.txt pos-test-key.txt > pos-taggingreport.txt
         
		The overall accuracy when rules are added is .85
		The overall accuracy when rules are not added and default tag is NN is .84
@Algorithim:
			1)The first argument, pos-tags.txt is read by the program and converted into list of tuples as[(word,tag)]The tag sequence is stored in a list y_pred 
		 2)The second argument, pos-test-key.txt is read by the program and converted into list of tuples as
		   [(word,tag)]. The tag sequence is stored in a list y_true
		3)Tag sequnece of predicted and actual are compared and confusion matrix is generated. Overall accurcy is 
		 calculated as (total number of correctly tagged/total tags)
		4)The result is stored in report.txt

"""
import argparse
import nltk
import ast
import copy, time, sys
from collections import Counter
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

def main():
	# get input: 

	parser = argparse.ArgumentParser()
	parser.add_argument("file",type = str,nargs='+')                       #to take files from command prompt

	args = parser.parse_args()
	pos_tag= open(args.file[0], 'r', encoding="utf8")			#get predicted results
	
	pos_test_key= open(args.file[1], 'rt', encoding="utf8")     #get actual/gold-std results
	
	key= pos_test_key.read().split()
	key_f = [nltk.tag.str2tuple(t) for t in key]
	key_fpair=[(word,tag) for (word,tag) in key_f if tag !=None]
	y_true = [i[1] for i in key_fpair]                          #get actual tags into list
	
	
	"""start working on predicted reults"""
	readlines=pos_tag.read()
	pos_tag.close()
	xc=ast.literal_eval(readlines)
	y_pred = [i[1] for i in xc]									#get predicted tags in file
	
	AS=accuracy_score(y_true,y_pred)							#create accuracy score
	CM=nltk.ConfusionMatrix(y_true, y_pred)						#create confusion matrix
	f=open(args.file[2],"w")									#get results into .txt
	f.write("Accuracy is:{}\n".format(str(AS)))
	f.write(str(CM))
	f.close()

	
	

if __name__== '__main__':
    main()