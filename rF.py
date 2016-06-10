# Standard scientific Python imports
import matplotlib.pyplot as plt
from data_statistics import *


# Import datasets, classifiers and performance metrics
from sklearn import datasets, svm, metrics
from sklearn import ensemble
from tools import *
def copy_claaifier(tree):
      newtree = ensemble.RandomForestClassifier(10)
      newtree.estimators_ = tree.estimators_
      newtree.classes_ = tree.classes_
      newtree.n_classes_ = tree.n_classes_
      newtree.n_outputs_ = tree.n_outputs_
      newtree.feature_importances_ = tree.feature_importances_
      newtree.oob_score_ = tree.oob_score_
      newtree.oob_decision_function_ = tree.oob_decision_function_
      return newtree      

# Prepare data
X,y = load_dataset()

#make features
special_words = get_special_words(2000)

#make training data
trainX,trainY=subSet(X,y,25000)
dataX = [features_vec(t,special_words) for t in trainX]
dataY = trainY

#make validation data
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

#prints the validation error
print(float(sum(prediction[i] == expected[i] for i in range(len(expected))))/len(expected))
