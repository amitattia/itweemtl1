#!usr/bin/python3

import pandas
import numpy


def load_dataset(filename='tweets.csv'):
    train = pandas.read_csv(filename, header = None)
    X, y = train[1], train[0]
    X = X.tolist()
    return X, y


def my_key(entry):
    return entry[1][11]


def get_special_words(num_of_special_words=100):
    unique_dict = {}
    word_bag = []
    word_countr = 0
    X, y = load_dataset('tweets.csv')
    num_posts_by_poster = [0] * 10

    for i in range(int(0.5 * len(X))):
        sen = X[i]
        words_list = sen.split()
        num_posts_by_poster[y[i]] += 1
        for word in words_list:
            word = word.lower()
            if word in unique_dict:
                unique_dict[word][0] += 1
                unique_dict[word][y[i] + 1] += 1
            else:
                unique_dict[word] = [0] * 12
                unique_dict[word][0] += 1
            word_bag.append(word)

    for entry in unique_dict:
        values = unique_dict[entry][1:-1]
        for i in range(len(values)):
            values[i] /= num_posts_by_poster[i]
            unique_dict[entry][i + 1] = values[i]
        m = numpy.max(values)
        mean = numpy.mean(values)
        unique_dict[entry][11] = m - mean

    sorted_unique_dictionary = sorted(unique_dict.items(), key = my_key, reverse = True)

    special_word = [None] * num_of_special_words
    for i in range(min(num_of_special_words, len(sorted_unique_dictionary))):
        var = numpy.var(sorted_unique_dictionary[i][1][1:])
        values = sorted_unique_dictionary[i][1][1:11]
        # for j in range(len(values)):
        # values[j] /= posts_num[j]
        special_word[i] = sorted_unique_dictionary[i][0]
    return special_word

if __name__ == '__main__':
    my_list = get_special_words(100)
    for i in range(len(my_list)):
        print(my_list[i])
