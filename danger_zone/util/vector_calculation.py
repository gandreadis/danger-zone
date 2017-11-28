import numpy as np


def normalize(np_array):
    return (1 / np.linalg.norm(np_array)) * np_array


def limit_length(np_array, max_length):
    if np.linalg.norm(np_array) > max_length:
        return max_length * normalize(np_array)
    else:
        return np_array
