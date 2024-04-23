import math
from collections import Counter
import numpy as np

def entropy(data):
    freqs = Counter(data)
    probs = np.array(list(freqs.values())) / len(data)
    entropy = -np.sum(probs * np.log2(probs))
    return entropy

def word_entropy(text):
    words = text.split()
    return entropy(words)

def conditional_entropy(text, order):
    sequences = {}
    for i in range(len(text) - order):
        sequence = text[i:i+order+1]
        if sequence[:-1] not in sequences:
            sequences[sequence[:-1]] = []
        sequences[sequence[:-1]].append(sequence[-1])

    conditional_entropies = []
    for next_chars in sequences.values():
        counts = np.array(list(Counter(next_chars).values()))
        probs = counts / len(next_chars)
        conditional_entropy = -np.sum(probs * np.log2(probs))
        conditional_entropies.append(len(next_chars) / len(text) * conditional_entropy)
    return np.sum(conditional_entropies)

def load_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def print_results(files):
    max_order = 4
    for filename in files:
        sample_text = load_file("dane/" + filename)  
        print("Plik:", filename)

        char_ent = entropy(sample_text)
        print("Entropia znaków:", char_ent)

        word_ent = word_entropy(sample_text)
        print("Entropia słów:", word_ent)

        for i in range(max_order):
            conditional_ent = conditional_entropy(sample_text, order=i)
            print(f"Entropia warunkowa rzędu {i+1}:", conditional_ent)

test_files = ["norm_wiki_en.txt", "norm_wiki_la.txt", "norm_wiki_eo.txt", "norm_wiki_et.txt", "norm_wiki_so.txt", "norm_wiki_ht.txt", "norm_wiki_nv.txt"]
sample_files = ["sample0.txt", "sample1.txt", "sample2.txt", "sample3.txt", "sample4.txt", "sample5.txt"]

print_results(test_files)
print_results(sample_files)
