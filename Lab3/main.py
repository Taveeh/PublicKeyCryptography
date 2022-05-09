import math

x_0 = 2


def f(x):
    return x * x + 1


def g(x, n):
    return f(x) % n


def gcd(x, n):
    return math.gcd(x, n)


def pollard(number):
    first = x_0
    second = g(first, number)
    arr = [first, second]
    i = 2
    while True:
        greatest_common_divisor = gcd(abs(arr[i - 1] - arr[i // 2 - 1]), number)
        if greatest_common_divisor == number:
            print('FAILURE')
            return
        if greatest_common_divisor != 1:
            print('Factors:', greatest_common_divisor, number // greatest_common_divisor)
            return
        first = g(second, number)
        second = g(first, number)
        arr.append(first)
        arr.append(second)
        i += 2


if __name__ == '__main__':
    # while True:/
        nr = 101 * 103 * 3
        pollard(nr)
