from collections import Counter
import re
import random

def load_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def count_word_freq(text):
    words = re.findall(r'\b\w+\b', text)
    word_counts = Counter(words)
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_word_counts

def generate_text(word_counts, total_words, length):
    words = []
    weights = []
    for word_count in word_counts:
        word, count = word_count
        words.append(word)
        weights.append(count)
    normalized_weights = [count / total_words for count in weights]
    
    generated_text = []
    for _ in range(length):
        word = random.choices(words, weights=normalized_weights)[0]
        generated_text.append(word)
    
    return ' '.join(generated_text)

text = load_file("dane/norm_wiki_sample.txt")

word_counts = count_word_freq(text)
total_words = sum(count for word, count in word_counts)

print("Najczęściej występujące słowa:")
for word, count in word_counts[:10]:
    percentage = (count / total_words) * 100
    print(f"{word}: {percentage:.2f}%")

top_10_percentage = sum(count for word, count in word_counts[:10]) / total_words * 100
print(f"\n10 najczęstszych słów stanowi {top_10_percentage:.2f}% wszystkich słów w tekście.")

generated_text = generate_text(word_counts, total_words, 100)
print("Wygenerowany ciąg słów:")
print(generated_text)