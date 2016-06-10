import pandas
import operator
import re
import numpy
from data_statistics import *

#loads the data
def load_dataset(filename='tweets.csv'):
    train = pandas.read_csv(filename, header=None)
    X, y = train[1], train[0]
    X = X.tolist()
    y = y.tolist()
    return X, y

#returns a sub set of X and y of size s from sh
def subSet(X, y, s, sh = 0):
    return X[sh:s+sh], y[sh:s+sh]

#return the number of tripple letters in the twit (aaa etc)
def num_of_twit_tripplets(twit):
    tripplets = 0
    words_list = twit.split()
    for word in words_list:
        tripplets += num_of_word_tripplets(word)
    return tripplets

#return the number of tripple letters in the word
def num_of_word_tripplets(word):
    return len(re.findall("([A-Za-z])\1\1+", word))

#return the number of upper case letters in word
def num_of_upper_letters(word):
    upper_case_letter = 0
    for letter in list(word):
        upper_case_letter += letter == letter.upper()
    return upper_case_letter

#return the number of upper case words in letter
def num_of_upper_word(twit):
    upper_case_words = 0
    words_list = twit.split()
    for word in words_list:
        upper_case_words += word == word.upper()
    return upper_case_words

#return the number of 2 dots in a row or more
def num_of_dots(twit):
    return len(re.findall("..+", twit))

#return the number of occurences of word in twit
def num_of_word(twit, word):
    return twit.count(word)

#return the length of the twit in letters num
def twit_len(twit):
    return len(twit.split(' '))

#return 1 if a in b and 0 otherwise
def isIn(a, b):
    if a in b:
        return 1
    return 0

#returns the number of exatcly one dor in a twit
def num_of_dot(twit):
        return len(re.findall("[^\.]\.[^\.]", twit))
    
#returns a vector with 1 if a name occures in the twit and 0 otherwise
def features_vec_names(twit):
    lTweet = twit.lower()
    return [isIn(i,lTweet) for i in names()]

#
def bad_features_vec(twit, words):
    return (-1)*significant_words(twit,words)

#return a vector of all the features
def features_vec(twit, words):
    return [num_of_dot(twit), num_of_word(twit, ','), num_of_word(twit, '\''), len(twit),num_of_word(twit, '#'), num_of_word(twit, '@'),
            num_of_word(twit, '!'), 'bama' in twit, 'nald' in twit,
            'lary' in twit, num_of_dots(twit), twit_len(twit), 'resident' in twit, 'ardash' in twit, '&amp' in twit,
            '1989' in twit, 'ball' in twit, 'Soul' in twit, num_of_upper_word(twit), num_of_twit_tripplets(twit)] + significant_words(twit,words) + features_vec_names(twit)


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

#return a vector with 1 if a word of special_words occurs in twit and 0 otherwise
def significant_words(twit,special_words):
	return [(special_words[i] in twit.lower()) for i in range(len(special_words))]

#return a vector of all names
def names():
    return ['donald', 'trump' ,'hillary' ,'clinton' ,'barack', 'obama' ,'bernie', 'sanders','taylor', 'swift','oprah', 'winfrey' ,'lance', 'armstrong','cher','shaquille' ,'ONeal','O`Neal','khloe', 'kardashian']

#return a vector of 10 vectors of the twits of each figure
def split_by_figure(X, y):
    ret = [[] for i in range(10)]
    for i in range(len(X)):
        ret[y[i]].append(X[i])
    return ret

#return a set of data with 50% from n of the data of figure and 50% the others
def get_figure_data(X,y,figure, n):
    figures_data = split_by_figure(X, y)
    ret = []
    ret.append([figures_data[figure][i] for i in range(int(n/2))])
    for i in range(10):
        if not i == figure:
            ret.append([figures_data[i][j] for j in range(int(n/18))])
    return ret

# def get_batch(X,y,i):
#     return tf.constant(X[i*BATCH_SIZE:(i+1)*BATCH_SIZE]),tf.constant(y[i*BATCH_SIZE:(i+1)*BATCH_SIZE])
# INPUT_SIZE = 10
# OUTPUT_SIZE = 10
# BATCH_SIZE = 10
# NUM_BATCHES = 10
