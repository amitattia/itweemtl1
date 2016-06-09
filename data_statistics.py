#!usr/bin/python3

import numpy as np
import pandas

class Poster:
    allowed_posters = ['Trump', 'Clinton', 'Obama', 'Bernie Sanders', 'Taylor Swift', 'Oprah',
                                     'Armstrong', 'Cher', 'Shaq', 'Kardashian']
    def __init__(self, poster):
        if poster in Poster.allowed_posters:
            self.poster = poster
            self.enum = Poster.allowed_posters.index(poster)
        else:
            self.poster = None
            self.enum = -1

    @staticmethod
    def is_valid_poster(poster):
        return poster in Poster.allowed_posters

    @staticmethod
    def get_poster_by_index(index):
        return Poster.allowed_posters[index]

class Word:
    def __init__(self, word):
        self.word = word
        self.count = 0
        self.word_count_by_poster = []
        for poster in Poster.allowed_posters:
            self.word_count_by_poster.append(0)
        self.word_distribution = {}
        self.mean = 0
        self.max = 0
        self.argmax = ''
        self.min = 0
        self.argmin = ''

    def use(self, poster):
        self.count += 1
        if Poster.is_valid_poster(poster):
            posterObj = Poster(poster)
            self.word_count_by_poster[posterObj.enum] += 1
        else:
            self.word_count_by_poster[poster] += 1

    def calculate_statistics(self, num_of_posts_by_poster):
        self.word_distribution = list(self.word_count_by_poster)
        for poster in Poster.allowed_posters:
            post_obj = Poster(poster)
            if num_of_posts_by_poster[post_obj.enum] is not 0:
                self.word_distribution[post_obj.enum] /= float(num_of_posts_by_poster[post_obj.enum])

        self.max = np.max(self.word_distribution)
        self.argmax = Poster.get_poster_by_index(np.argmax(self.word_distribution))
        self.min = np.min(self.word_distribution)
        self.argmin = Poster.get_poster_by_index(np.argmin(self.word_distribution))
        self.mean = np.mean(self.word_distribution)

    def __str__(self):
        string = self.word + ' ' + str(self.count) + ' '
        string += str(self.word_distribution) + '\n'
        string += 'max: ' + str(self.max) + ' at: ' + self.argmax+ '\n'
        string += 'min: ' + str(self.min) + ' at: ' + self.argmin + '\n'
        string += 'mean: ' + str(self.mean)
        return string

def load_dataset(filename='tweets.csv', percentage=0.5):
    train = pandas.read_csv(filename, header = None)
    X, y = train[1], train[0]
    X = X.tolist()
    return X[:int(len(X)*percentage)], y[:int(len(X) * percentage)]


def gather_data(tweets, posters):
    num_posts_by_poster = [0] * len(Poster.allowed_posters)
    word_container = {}
    # split tweets
    for i in range(len(tweets)):
        sen = tweets[i]
        num_posts_by_poster[posters[i]] += 1
        for word in sen.split():
            word = word.lower()
            if word not in word_container:
                word_container[word] = Word(word)
            word_container[word].use(Poster.get_poster_by_index(posters[i]))
    for word in word_container.values():
        word.calculate_statistics(num_posts_by_poster)
    print(num_posts_by_poster)
    return word_container


def get_special_words(words, size=10, key=None, poster=None, epsilon=0.0):
    sorted_words = sorted(words.values(), key = key)
    special_words = []
    counter = 0
    for w in sorted_words:
        if counter is size:
            return special_words
        if w.word_distribution[Poster(w.argmax).enum] >= epsilon:
            if poster is not None:
                if w.argmax is poster:
                    special_words.append(w)
                    counter += 1
            else:
                special_words.append(w)
                counter += 1
    return special_words


def get_good_words(xTrain, yTrain, good_words_size=10, good_words_epsilon=0.02):
    words = gather_data(xTrain, yTrain)
    good_words = []
    for poster in Poster.allowed_posters:
        good_words += get_special_words(words, poster = poster, size = good_words_size, key = lambda word: -1 * (word.max - word.mean), epsilon = good_words_epsilon)
    return [w.word for w in good_words]



