import numpy as np
import random


def get_q_indexes(values, bins):
    indexes = np.zeros(len(values))
    for i in range(len(values)):
        if values[i] <= bins[i][0]:
            indexes[i] = 0
        elif values[i] >= bins[i][-1]:
            indexes[i] = len(bins[i]) - 1
        else:
            indexes[i] = np.digitize([values[i]], bins[i])[0] - 1
    return indexes


def weighted_choice(weights):
    choice = random.random() * sum(weights)
    for i, w in enumerate(weights):
        choice -= w
        if choice < 0:
            return i