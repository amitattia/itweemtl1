# Standard scientific Python imports
import matplotlib.pyplot as plt
from data_statistics import *


# Import datasets, classifiers and performance metrics
from sklearn import datasets, svm, metrics
from sklearn import ensemble
from tools import *

def setLabels(y,i):
      return [1 if j == i else 0 for j in y]


def setG(y, i):
    return [1 if j == i else 0 for j in y]

# special_words = get_special_words(1000)
# X,y = load_dataset()
# trainX,trainY=subSet(X,y,12000)
# gX = list(subX)
# gY = [yToGroup(t) for t in subY.tolist()]
# dataX = [features_vec(t,special_words) for t in gX]
# dataY = gY
# dataX = [features_vec(t,special_words) for t in subX]
# dataY = subY

special_words = get_special_words(1000)
X,y = load_dataset()
trainX,trainY=subSet(X,y,15000)
#special_words = get_good_words(trainX,trainY,good_words_size=200)
dataX = [features_vec(t,special_words) for t in trainX]
dataY = trainY
testX,testY=subSet(X,y,5000,15000)
dataTestX = [features_vec(t,special_words) for t in testX]
dataTestY = testY
# Create a classifier
classifier = ensemble.RandomForestClassifier(10)

# We learn the digits on the first half of the digits
classifier.fit(dataX, dataY)

# Now predict the value of the digit on the second half:
expected = dataTestY
predicted = classifier.predict(dataTestX)

print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(expected, predicted)))
