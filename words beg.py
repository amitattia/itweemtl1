#!usr/bin/python3
import pandas
import operator

def load_dataset(filename='tweets.csv'):
    train = pandas.read_csv(filename, header = None)
    X, y = train[1], train[0]
    X = X.tolist()
    return X, y

unique_dict = {}
word_bag = []
word_countr = 0
X, y = load_dataset('tweets.csv')
for sen in X:
    words_list = sen.split()
    for word in words_list:
        if word in unique_dict:
            unique_dict[word] += 1
        else:
            unique_dict[word] = 1
        word_bag.append(word)
print('unique length ' + str(len(unique_dict)))
print('number of words ' + str(len(word_bag)))
# print('words: ')
# for key in unique_dict.keys():
#     print(key + " --> " + str(unique_dict[key]))

sorted_unique_dictionary = sorted(unique_dict, key = unique_dict.get)
print('words: ')
for i in range(len(sorted_unique_dictionary)):
    print(sorted_unique_dictionary[-(i + 1)] + " --> " + str(unique_dict[sorted_unique_dictionary[-(i + 1)]]))
