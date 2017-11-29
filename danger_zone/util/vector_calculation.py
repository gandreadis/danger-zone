import math

import numpy as np


def normalize(np_array):
    return (1 / np.linalg.norm(np_array)) * np_array


def limit_length(np_array, max_length):
    if np.linalg.norm(np_array) > max_length:
        return max_length * normalize(np_array)
    else:
        return np_array


def get_vector_angle(np_array):
    v1_u = normalize(np_array)
    v2_u = np.array([0, 1])
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)) * (180 / math.pi)
