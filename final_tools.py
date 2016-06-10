import numpy as np

def names():
    return ['donald', 'trump', 'hillary', 'clinton', 'barack', 'obama', 'bernie', 'sanders', 'taylor', 'swift', 'oprah',
            'winfrey', 'lance', 'armstrong', 'cher', 'shaquille', 'ONeal', 'O`Neal', 'khloe', 'kardashian']


def get_features(data_x, words):
    def is_inside(name,tweet):
        if name in tweet:
            return 1
        return 0
    feats = []
    for i in range(len(data_x)):
        feats.append([is_inside(n, data_x[i]) for n in words])
    #print(np.mean([sum(i) for i in feats]))
    return feats


def get_err(p, e):
    s = sum(p[i] == e[i] for i in range(len(e)))
    return float(s) / len(e)
