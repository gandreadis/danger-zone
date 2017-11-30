import numpy as np


def normalize(np_array):
    return (1 / np.linalg.norm(np_array)) * np_array


def limit_length(np_array, max_length):
    if np.linalg.norm(np_array) > max_length:
        return max_length * normalize(np_array)
    else:
        return np_array


def calculate_angle_between(p1, p2):
    angle_1 = np.arctan2(*p1[::-1])
    angle_2 = np.arctan2(*p2[::-1])

    return np.rad2deg((angle_1 - angle_2) % (2 * np.pi))


REFERENCE_VECTOR = np.array([0, 1])


def get_vector_angle(np_array):
    return calculate_angle_between(REFERENCE_VECTOR, np_array)
