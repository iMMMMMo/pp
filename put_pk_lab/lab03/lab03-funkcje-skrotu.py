import hashlib
import random
import string
import time
import matplotlib.pyplot as plt
import numpy as np

algorithms = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512']
def main():
    text_input = input("Enter text: ")
    for algorithm in algorithms:
        print(f"{algorithm.upper()} hash: {generate_hash(text_input, algorithm)}")
    
    data = [''.join(random.choices(string.ascii_letters, k=random.randint(500, 1000))) for _ in range(100000)]
    average_times, average_lengths = calculate_average_speed_and_length(data)
    
    plt.figure(figsize=(10, 5))
    plt.bar(algorithms, [average_times[alg] for alg in algorithms], color='blue')
    plt.xlabel('Algorytm')
    plt.ylabel('Średni czas (us)')
    plt.title('Średnie czasy hashowania dla różnych algorytmów')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.bar(algorithms, [average_lengths[alg] for alg in algorithms], color='green')
    plt.xlabel('Algorytm')
    plt.ylabel('Średnia ilość znaków')
    plt.title('Średnie długości hashów dla różnych algorytmów')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


    for algorithm in average_times:
        print(f"Algorithm: {algorithm.upper()}, Average Time: {average_times[algorithm]:.7f} s, Average Length: {average_lengths[algorithm]} chars")
    
    collision_on_first_12_bits('md5')

    text_input2 = input("Enter second text: ")

    for algorithm in algorithms:
        print(f"For {algorithm.upper()} bits change prob equals {check_bit_flip_probability(text_input, text_input2, algorithm)}")

def generate_hash(text, algorithm):
    if algorithm.lower() == 'md5':
        return hashlib.md5(text.encode()).hexdigest()
    elif algorithm.lower() == 'sha1':
        return hashlib.sha1(text.encode()).hexdigest()
    elif algorithm.lower() == 'sha224':
        return hashlib.sha224(text.encode()).hexdigest()
    elif algorithm.lower() == 'sha256':
        return hashlib.sha256(text.encode()).hexdigest()
    elif algorithm.lower() == 'sha384':
        return hashlib.sha384(text.encode()).hexdigest()
    elif algorithm.lower() == 'sha512':
        return hashlib.sha512(text.encode()).hexdigest()
    elif algorithm.lower() == 'sha3_224':
        return hashlib.sha3_224(text.encode()).hexdigest()
    elif algorithm.lower() == 'sha3_256':
        return hashlib.sha3_256(text.encode()).hexdigest()
    elif algorithm.lower() == 'sha3_384':
        return hashlib.sha3_384(text.encode()).hexdigest()
    elif algorithm.lower() == 'sha3_512':
        return hashlib.sha3_512(text.encode()).hexdigest()
    else:
        return "Invalid algorithm"

def calculate_average_speed_and_length(data):
    average_times = {}
    average_lengths = {}
    for algorithm in algorithms:
        start_time = time.time()
        total_length = 0
        for text in data:
            hash_result = generate_hash(text, algorithm)
            total_length += len(hash_result)
        end_time = time.time()
        average_times[algorithm] = (end_time - start_time) / len(data)
        average_lengths[algorithm] = total_length / len(data)
    return average_times, average_lengths

def collision_on_first_12_bits(algorithm):
    hashes = set()
    ctr = 0
    while True:
        text = ''.join(random.choices(string.ascii_letters, k=8))
        hash_value = generate_hash(text, algorithm)[:3]
        ctr += 1
        if hash_value in hashes:
            print(f"Found collision for {algorithm} on first 12 bits after {ctr} tests")
            break
        else:
            hashes.add(hash_value)

        if ctr > 10000:
            print(f"Didnt find any collisions for {algorithm} on first 12 bits after {ctr} tests")
            break
    return

def check_bit_flip_probability(text1, text2, algorithm):
    hash1 = generate_hash(text1, algorithm)
    hash2 = generate_hash(text2, algorithm)

    if len(hash1) != len(hash2):
        return False

    bit_flips = 0
    for char1, char2 in zip(hash1, hash2):
        xor_result = int(char1, 16) ^ int(char2, 16)
        bit_flips += bin(xor_result).count('1')

    return bit_flips / (len(hash1) * 4)

if __name__ == "__main__":
    main()
