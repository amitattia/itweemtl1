import pandas
import operator
import re
import numpy

def load_dataset(filename='tweets.csv'):
    train = pandas.read_csv(filename, header = None)
    X, y = train[1], train[0]
    X = X.tolist()
    return X, y

X, y = load_dataset('tweets.csv')


#counts upper case words and letters
def count_upper_words_and_letters():
	upper_case_words = [0]*10
	upper_case_letters = [0]*10
	for i in range(int(0.75 * len(X))):
		twit = X[i]
		words_list = twit.split()
		for word in words_list:
			upper_case_words[y[i]] += word == word.upper()
			for letter in list(word):
				upper_case_letters[y[i]] += letter == letter.upper()
	return upper_case_words, upper_case_letters
	
#makes special letters dictionary
def make_special_letters_dict():
	unique_special_dict = {}
	special_letters_bag = []
	for i in range(int(0.75 * len(X))):
		twit = X[i]
		words_list = twit.split()
		for word in words_list:
			for letter in list(word):
				if not letter.isalnum():
					if letter in unique_special_dict:
						unique_special_dict[letter][0] += 1
						unique_special_dict[letter][y[i] + 1] += 1
					else:
						unique_special_dict[letter] = [0]*11
						unique_special_dict[letter][0] += 1
					special_letters_bag.append(letter)
	return unique_special_dict


def num_of_twit_tripplets(twit):
    tripplets = 0
    words_list = twit.split()
    for word in words_list:
         tripplets += num_of_word_tripplets(word)
    return tripplets
def num_of_word_tripplets(word):
	return len(re.findall("([A-Za-z])\1\1+", word))
def num_of_tripplets(twit):
	return len(re.findall("([A-Za-z])\1\1+", word))
def num_of_upper_letters(word):
	upper_case_letter = 0
	for letter in list(word):
		upper_case_letter += letter == letter.upper()
	return upper_case_letter
def num_of_upper_word(twit):
    upper_case_words = 0
    words_list = twit.split()
    for word in words_list:
        upper_case_words += word == word.upper()
    return upper_case_words
def num_of_dots(twit):
	return len(re.findall("..+", twit))
def num_of_word(twit, word):
	return twit.count(word)
def twit_len(twit):
	return len(twit.split(' '))

def features_vec(twit):
	return [num_of_word(twit,'#'), num_of_word(twit,'@'), num_of_word(twit,'!'), 'bama' in twit, 'nald' in twit, 'lary' in twit, num_of_dots(twit), twit_len(twit)]





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






def significant_words(twit, num_of_special_words=100):
	special_words = get_special_words(num_of_special_words)
	return [(special_words[i] in twit) for i in range(len(special_words))]
