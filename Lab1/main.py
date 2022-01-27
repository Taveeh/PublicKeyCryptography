import math
from functools import reduce
import random


def compute_gcd_prime_factors(array):
    """
    Compute the GCD by doing the product of the common prime factors at the lowest power
    :param array: the array of numbers to compute their GCD
    :return: greatest_common_divisor - number
    """
    divisors_power = {}
    minimum = min(array)
    for number in array:
        copy_number = number
        if number == 0:
            continue
        for divisor in range(2, minimum + 1):
            cnt = 0
            if divisor not in divisors_power:
                divisors_power[divisor] = math.inf
            while copy_number % divisor == 0:
                copy_number //= divisor
                cnt += 1
            divisors_power[divisor] = min(divisors_power[divisor], cnt)

    greatest_common_divisor = 1
    for divisor in divisors_power:
        greatest_common_divisor *= divisor ** divisors_power[divisor]
    return greatest_common_divisor


def python_gcd(array):
    return reduce(math.gcd, array)


def test_algorithm():
    n = random.randint(3, 10000)
    array = []
    for _ in range(n):
        array.append(random.randint(0, 200000))

    py_gcd = python_gcd(array)
    my_gcd = compute_gcd_prime_factors(array)
    if py_gcd != my_gcd:
        print(array)
        print(py_gcd)
        print(my_gcd)
        assert False


if __name__ == '__main__':
    arr = [18, 90, 12, 36]
    print(compute_gcd_prime_factors(arr))
    print(python_gcd(arr))
    for i in range(200):
        test_algorithm()
