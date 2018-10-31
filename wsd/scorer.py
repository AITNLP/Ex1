import sys
import re
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

if __name__ == "__main__":
    true_file = sys.argv[1]
    pred_file = sys.argv[2]
    pattern = 'senseid="(\w+)"'
    with open(true_file) as F1, open(pred_file) as F2:
        true_data  = [re.search(pattern, line).group(1) for line in F1.readlines() if re.search(pattern, line)]
        pred_data = [re.search(pattern, line).group(1) for line in F2.readlines() if re.search(pattern, line)]
    labels = ['phone', 'product']
    print("Confusion matrix:= ", confusion_matrix(true_data, pred_data, labels=labels))
    print("Accuracy := ", accuracy_score(true_data, pred_data))

# Test python scorer.py line-answer.txt my-line-answer.txt