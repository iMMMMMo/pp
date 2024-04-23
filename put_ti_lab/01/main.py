import random
import re
from collections import defaultdict

def load_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def generate_markov_chain(text, order):
    markov_chain = defaultdict(list)
    for i in range(len(text) - order):
        prefix = text[i:i+order]
        suffix = text[i+order]
        markov_chain[prefix].append(suffix)
    return markov_chain

def generate_text(markov_chain, length, seed=None):
    if seed is not None:
        random.seed(seed)
    prefix = random.choice(list(markov_chain.keys()))
    text = list(prefix)
    for _ in range(length - len(prefix)):
        suffix = random.choice(markov_chain[prefix])
        text.append(suffix)
        prefix = prefix[1:] + suffix
    return ''.join(text)

def avg_word_length(text):
    words = re.findall(r'\b\w+\b', text)
    if words:
        return sum(len(word) for word in words) / len(words)
    return 0

text = load_file("dane/norm_hamlet.txt")

order_1_chain = generate_markov_chain(text, 1)
markov_text_order_1 = generate_text(order_1_chain, 1000)

order_3_chain = generate_markov_chain(text, 3)
markov_text_order_3 = generate_text(order_3_chain, 1000)

starting_text = "probability"
order_5_chain = generate_markov_chain(text, 5)
markov_text_order_5 = generate_text(order_5_chain, 1000, seed=starting_text)

avg_word_length_order_1 = avg_word_length(markov_text_order_1)
avg_word_length_order_3 = avg_word_length(markov_text_order_3)
avg_word_length_order_5 = avg_word_length(markov_text_order_5)

print("Przybliżenie źródła Markova pierwszego rzędu:")
print(markov_text_order_1)
print("Średnia długość wyrazu:", avg_word_length_order_1)

print("\nPrzybliżenie źródła Markova trzeciego rzędu:")
print(markov_text_order_3)
print("Średnia długość wyrazu:", avg_word_length_order_3)

print("\nPrzybliżenie źródła Markova piątego rzędu:")
print(markov_text_order_5)
print("Średnia długość wyrazu:", avg_word_length_order_5)