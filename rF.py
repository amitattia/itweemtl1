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

# Prepare data
X,y = load_dataset()
trainX,trainY=subSet(X,y,25000)
special_words = get_special_words(2000)
dataX = [features_vec(t,special_words) for t in trainX]
dataY = trainY
testX,testY=subSet(X,y,5000,25000)
dataTestX = [features_vec(t,special_words) for t in testX]
dataTestY = testY

# Create a classifier
classifier = ensemble.RandomForestClassifier(10)

# We learn the digits on the first half of the digits
classifier.fit(dataX, dataY)

# Now predict the value of the digit on the second half:
expected = dataTestY
prediction = classifier.predict(dataTestX)

print(float(sum(prediction[i] == expected[i] for i in range(len(expected))))/len(expected))
