import numpy as np

n = 27
m = 2
k = np.matrix('11 8; 3 7')
inv_k = np.matrix('20 8; 3 16')
dictionary = {
    ' ': 0,
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'f': 6,
    'g': 7,
    'h': 8,
    'i': 9,
    'j': 10,
    'k': 11,
    'l': 12,
    'm': 13,
    'n': 14,
    'o': 15,
    'p': 16,
    'q': 17,
    'r': 18,
    's': 19,
    't': 20,
    'u': 21,
    'v': 22,
    'w': 23,
    'x': 24,
    'y': 25,
    'z': 26,
}

reverse_dictionary = {value: key for key, value in dictionary.items()}


def encrypt(message, matrix):
    words = [message[i:i + m] for i in range(0, len(message), m)]
    if len(words[-1]) == 1:
        words[-1] += ' '
    res = ''
    for word in words:
        word_matrix = np.matrix([dictionary[word[0]], dictionary[word[1]]])
        result_matrix = (word_matrix * matrix).tolist()[0]
        result_matrix = [el % n for el in result_matrix]
        res += reverse_dictionary[result_matrix[0]] + reverse_dictionary[result_matrix[1]]
    return res


print(encrypt('cartofior', k))
print(encrypt('idonu ioii', inv_k))
