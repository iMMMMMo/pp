import string
import random
import re
from collections import Counter

alfabet = list(string.ascii_lowercase)
alfabet.append(' ')

def load_file(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        print("Cannot load file: ", e)
        return

def generate(size, probabilities=None):
    if probabilities is None:
        probabilities = {char: 1/len(alfabet) for char in alfabet}

    weights = list(probabilities.values())

    generated_string = []
    for _ in range(size):
        generated_string.append(random.choices(alfabet, weights=weights)[0])

    return ''.join(generated_string)

def count_avg_word_len(text):
    text = re.sub(r'\s+', ' ', text.strip())

    words = text.split(' ')
    sum_word_lengths = sum(len(word) for word in words)

    if len(words) > 0:
        avg_word_length = sum_word_lengths / len(words)
        return avg_word_length
    else:
        return 0

def check_letters_freq(text):
    freq = {char: 0 for char in alfabet}
    for c in set(text):
        if c in alfabet:
            freq[c] = text.count(c) / len(text)
    return freq

def calculate_conditional_probabilities(text):
    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    bigram_counts = Counter(bigrams)

    most_common_chars = Counter(text).most_common()
    second_most_common_char = most_common_chars[1][0]

    conditional_probabilities = {char: 0 for char in alfabet if char != second_most_common_char}
    for char in set(text):
        if char != ' ' and char != second_most_common_char:
            bigram = second_most_common_char + char
            bigram_count = bigram_counts.get(bigram, 0)
            char_count = text.count(char)
            conditional_probabilities[char] = bigram_count / char_count

    return (conditional_probabilities, second_most_common_char)

if __name__ == "__main__":
    text = generate(1000000)
    print("Average word length: ", count_avg_word_len(text))

    text_from_file = load_file("dane/norm_romeo.txt")
    letters_freq = check_letters_freq(text_from_file)
    for char, probability in letters_freq.items():
        print(f"Prawdopodobieństwo wystąpienia znaku {char} wynosi: {probability}")

    text2 = generate(1000000, letters_freq)
    print("Average word length: ", count_avg_word_len(text2))

    conditional_probabilities, second_most_common_char = calculate_conditional_probabilities("beekeepers keep bees in a beehive")
    print("Drugi najczesciej wystepujacy znak w tekscie: ", second_most_common_char)
    for char, probability in conditional_probabilities.items():
        print(f"Prawdopodobieństwo wystąpienia znaku {char} po drugim najczęściej występującym znaku: {probability}")