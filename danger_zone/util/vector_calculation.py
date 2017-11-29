import numpy as np


def normalize(np_array):
    return (1 / np.linalg.norm(np_array)) * np_array


def limit_length(np_array, max_length):
    if np.linalg.norm(np_array) > max_length:
        return max_length * normalize(np_array)
    else:
        return np_array


def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))


def get_vector_angle(np_array):
    return angle_between(np.array([0, 1]), np_array)
