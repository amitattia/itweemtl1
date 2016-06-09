import pandas
import operator
import re

def load_dataset(filename='tweets.csv'):
    train = pandas.read_csv(filename, header = None)
    X, y = train[1], train[0]
    X = X.tolist()
    return X, y

X, y = load_dataset('tweets.csv')



# counts !
exp_mark = [0]*10
for i in range(int(0.75 * len(X))):
    twit = X[i]
    exp_mark[y[i]] += twit.count('!')

# count ..+
dots = [0]*10
for i in range(int(0.75 * len(X))):
    twit = X[i]
    dots[y[i]] += len(re.findall("..+", twit))

#counts upper case words and letters
upper_case_words = [0]*10
upper_case_letters = [0]*10
for i in range(int(0.75 * len(X))):
    twit = X[i]
    words_list = twit.split()
    for word in words_list:
        upper_case_words[y[i]] += word == word.upper()
        for letter in list(word):
            upper_case_letters[y[i]] += letter == letter.upper()
	
#makes special letters dictionary
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

#tripple_letters
tripple_letter_words = [0]*10
for i in range(int(0.75 * len(X))):
    twit = X[i]
    words_list = twit.split()
    for word in words_list:
        tripple_letter_words[y[i]] += len(re.findall("([A-Za-z])\1\1+", word))

#length
twit_length = [0]*10
num_of_twits = [0]*10
for i in range(int(0.75 * len(X))):
	twit = X[i]
	twit_length[y[i]] += len(twit.split(' '))
	num_of_twits[y[i]] += 1
print([float(twit_length[i])/num_of_twits[i] for i in range(len(twit_length))])


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
