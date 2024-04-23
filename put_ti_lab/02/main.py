import random
from collections import defaultdict

def load_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def generate_markov_chain(text, order):
    markov_chain = defaultdict(list)
    words = text.split()
    for i in range(order, len(words)):
        prefix = ' '.join(words[i-order:i])
        suffix = words[i]
        markov_chain[prefix].append(suffix)
        
    return markov_chain

def generate_text(markov_chain, length, seed=None):
    if seed is not None:
        prefix = seed
    else:
        prefix = random.choice(list(markov_chain.keys()))
    text = prefix.split()
    order = len(text)
    while len(text) < length:
        if prefix not in markov_chain:
            break
        suffix = random.choice(markov_chain[prefix])
        text.append(suffix)
        prefix = ' '.join(text[-order:])
    return ' '.join(text)


def main():
    text = load_file("dane/norm_wiki_sample.txt")

    order_1_chain = generate_markov_chain(text, 1)
    markov_text_order_1 = generate_text(order_1_chain, 1000)

    print("Przybliżenie źródła Markova pierwszego rzędu:")
    print(markov_text_order_1)

    order_2_chain = generate_markov_chain(text, 2)

    markov_text_order_2 = generate_text(order_2_chain, 1000)

    starting_text = "probability of"
    markov_text_order_2_with_starting_text = generate_text(order_2_chain, 1000, seed=starting_text)

    print("\nPrzybliżenie źródła Markova drugiego rzędu:")
    print(markov_text_order_2)

    print("\nPrzybliżenie źródła Markova drugiego rzędu (zaczynając od słowa 'probability of'):")
    print(markov_text_order_2_with_starting_text)

if __name__ == "__main__":
    main()
