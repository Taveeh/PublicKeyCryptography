import math
import random
import time

private_key = (0, 0, 0)
public_key = 0

message = "amo la criptografia"


def fast_exponentiation(g: int, a: int, p: int, m: int = -1) -> int:
    result = 1
    while a:
        if a % 2 == 1:
            result = (result * g) % p
        g = (g * g) % p
        a //= 2

    if m != -1:
        result = (m * result) % p
    return result


def isPrime(x):
    if x % 2 == 0:
        return False
    i = 3
    while i * i <= x:
        if x % i == 0:
            return False
        i += 2
    return True


def generate_large_random_prime() -> int:
    lower_bound = 43424324324
    upper_bound = 2432423432324
    starting_point = random.randint(lower_bound, upper_bound)
    potential_prime = starting_point * 2 + 1
    while not isPrime(potential_prime):
        potential_prime += 2
    return potential_prime


# noinspection PyBroadException
def find_generator(p: int) -> int:
    for potential_generator in range(2, p):
        visited = {}
        group_member = 1
        found_generator = True
        for _ in range(1, p):
            group_member = (group_member * potential_generator) % p
            try:
                if visited[group_member] == 1:
                    found_generator = False
            except Exception:
                visited[group_member] = 1
        if found_generator:
            return potential_generator
    raise ArithmeticError("p is not prime")


def prime_factorisation(nr: int) -> {int: int}:
    result = {}
    while nr % 2 == 0:
        if 2 in result.keys():
            result[2] += 1
        else:
            result[2] = 1
        nr //= 2

    for i in range(3, int(math.sqrt(nr)) + 1, 2):
        while nr % i == 0:
            if i in result.keys():
                result[i] += 1
            else:
                result[i] = 1
            nr //= i
    if nr > 2:
        result[nr] = 1
    return result


def find_generator_faster_hopefully(p: int) -> int:
    cardinal_of_group = p - 1
    factorisation = prime_factorisation(cardinal_of_group)
    print(cardinal_of_group)
    print(factorisation.keys())
    for potential_generator in range(p - 1, 2, -1):
        is_generator = True
        for i in factorisation.keys():
            if fast_exponentiation(potential_generator, cardinal_of_group // i, p) == 1:
                is_generator = False
                break
        if is_generator:
            return potential_generator
    raise ArithmeticError("P is not prime")


def generate_private_key(p: int) -> int:
    return random.randint(1, p - 2)


def generate_keys() -> ((int, int, int), int):
    p = generate_large_random_prime()
    start = time.time()
    g = find_generator_faster_hopefully(p)
    end = time.time()
    print(f"Finding {g} took {end - start}")

    # start = time.time()
    # g = find_generator(p)
    # end = time.time()
    # print(f"Finding {g} took {end - start}")

    a = generate_private_key(p)
    gap = fast_exponentiation(g, a, p)  # g^a mod p
    return (p, g, gap), a


def encrypt(m: int, public_key: (int, int, int)) -> (int, int):
    #  public_key is (p, g, g^a)
    k = generate_private_key(public_key[0])
    alpha = fast_exponentiation(public_key[1], k, public_key[0])
    beta = fast_exponentiation(public_key[2], k, public_key[0], m)
    return alpha, beta


def decrypt(c: (int, int), private_key: int, p: int) -> int:
    #  c is (alpha, beta)
    return fast_exponentiation(c[0], p - 1 - private_key, p, c[1])


def encode_text(word: str, key: int, p: int = 27) -> (int, int):
    value = 0
    current = 0
    key -= 1
    for character in word:
        if character != ' ':
            value += (ord(character) - ord('a') + 1) * (p ** current)
        current += 1
    quotient = 0
    if value > key:
        quotient = value // key
        value = value % key
    return value, quotient


def decode_text(encoded_value: int, key: int, quotient: int = 0, p: int = 27) -> str:
    res = ""
    key -= 1
    encoded_value += key * quotient
    while encoded_value != 0:
        char = encoded_value % p
        if char == 0:
            res += ' '
        else:
            res += chr(char + ord('a') - 1)
        encoded_value //= p
    return res


def test():
    for i in range(10000):
        pub_key, priv_key = generate_keys()
        rem, quot = encode_text(message, pub_key[0])  # message,  0 < m < p-1
        encoded = encrypt(rem, pub_key)
        decoded = decrypt(encoded, priv_key, pub_key[0])
        assert decode_text(decoded, pub_key[0], quot) == message


if __name__ == '__main__':
    # test()
    print("\nMessage to be sent:\t", message)
    # Key generation
    print("\nGenerated keys:")
    public_key, private_key = generate_keys()
    print("Public key (p, g, g^a):\t", public_key)
    print("Private key:\t", private_key)

    # Encryption
    print("\nBobby encrypts his dank message:")
    remainder, quotient = encode_text(message, public_key[0])  # message,  0 < m < p-1
    c = encrypt(remainder, public_key)  # cyphertext
    print("Encoded number:\t", c)
    print("Encoded text:\t", decode_text(c[0], public_key[0], quotient) + decode_text(c[1], public_key[0], quotient))
    # Decryption
    print("\nAlice get the dank message in the Wonderland and decrypts it:")
    plaintext = decrypt(c, private_key, public_key[0])
    print("Decoded message:\t", decode_text(plaintext, public_key[0], quotient))
    print("\nblaze it\n")
