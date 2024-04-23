import random

def main():
    n = generate_prime()
    g = primRoot(n)
    print(g)
    x = random.randint(2, n - 1)
    y = random.randint(2, n - 1)
    
    X = calculate_public_key(x, g, n)
    Y = calculate_public_key(y, g, n)
    
    session_key_A = pow(Y, x, n)
    session_key_B = pow(X, y, n)
    
    print("Klucz sesji obliczony przez A:", session_key_A)
    print("Klucz sesji obliczony przez B:", session_key_B)

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

def primRoot(modulo):
    required_set = set(num for num in range (1, modulo) if gcd(num, modulo) == 1)

    for g in range(1, modulo):
        actual_set = set(pow(g, powers, modulo) for powers in range (1, modulo))
        if required_set == actual_set:
            return g         
    return 0

def calculate_public_key(private_key, base, prime):
    return pow(base, private_key, prime)

if __name__ == "__main__":
    main()