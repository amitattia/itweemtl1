from sklearn import metrics
from sklearn import ensemble
from tools import load_dataset
from final_tools import *
import tools

words = tools.get_special_words(2000)
X, y = load_dataset()

x_train = X[:19000]
y_train = y[:19000]
x_val = X[19000:22000]
y_val = y[19000:22000]
x_test = X[22000:]
y_test = y[22000:]

train_features = get_features(x_train, words)
test_features = get_features(x_val, words)

classifier = ensemble.RandomForestClassifier()
classifier.fit(train_features, y_train)

expected = y_val
predicted = classifier.predict(test_features)
print(get_err(predicted, expected))
