import random

def main():

    public_key, private_key = generate_keys()

    message = "Przygotować dwie czterocyfrowe liczby pierwsze p i q"

    encrypted_message = encrypt(message, public_key)

    decrypted_message = decrypt(encrypted_message, private_key)

    print("\nOryginalna wiadomość:", message)
    print("\nZaszyfrowana wiadomość: ", encrypted_message)
    print("\nOdszyfrowana wiadomość:", decrypted_message)

def is_prime(num):
    if num > 1:
        for i in range(2, int(num/2)+1):
            if (num % i) == 0:
                return False
        return True
    else:
        return False
    
def generate_prime():
    prime = random.randint(1000, 9999)
    while not is_prime(prime):
        prime = random.randint(1000, 9999)
    return prime

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def generate_keys():
    p = generate_prime()
    q = generate_prime()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randint(2, 9999)
    while gcd(e, phi) != 1 or not is_prime(e):
        e = random.randint(2, 9999)
    d = pow(e, -1, phi)
    return (e, n), (d, n)

def encrypt(message, public_key):
    e, n = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

def decrypt(encrypted_message, private_key):
    d, n = private_key
    decrypted_message = ''.join([chr(pow(char, d, n)) for char in encrypted_message])
    return decrypted_message

if __name__ == "__main__":
    main()

# Pyt 1: trudne w realizacji jest wylosowanie duzych liczb pierwszych jak i ustalenie odpowiednich wartosci dla parametrow e i d
# Pyt 2: o bezpieczenstwie i jakosci tego algorytmu stanowia dlugosci parametrow p i q