import bitarray
import pickle
import os

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

def create_priority_queue(frequencies):
    return sorted([HuffmanNode(char, freq) for char, freq in frequencies.items()], key=lambda x: x.freq)

def pop_min(queue):
    return queue.pop(0)

def insert_queue(queue, node):
    queue.append(node)
    queue.sort(key=lambda x: x.freq)

def create_huffman_tree(frequencies):
    queue = create_priority_queue(frequencies)
    
    while len(queue) > 1:
        node1 = pop_min(queue)
        node2 = pop_min(queue)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        insert_queue(queue, merged)
    
    return queue[0]

def create_codes(node, prefix="", code={}):
    if node is not None:
        if node.char is not None:
            code[node.char] = prefix
        create_codes(node.left, prefix + "0", code)
        create_codes(node.right, prefix + "1", code)
    return code

def encode(text, code):
    encoded_text = bitarray.bitarray()
    for char in text:
        encoded_text.extend(code[char])
    return encoded_text

def decode(encoded_text, code, original_length):
    reversed_code = {v: k for k, v in code.items()}
    decoded_text = ""
    current_code = ""
    bit_count = 0
    for bit in encoded_text:
        current_code += '1' if bit else '0'
        if current_code in reversed_code:
            decoded_text += reversed_code[current_code]
            current_code = ""
            bit_count += 1
        if bit_count == original_length:
            break
    return decoded_text

def save(code, encoded_text, filename, original_length):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as file:
        pickle.dump((code, original_length), file)
        file.write(encoded_text.tobytes())

def load(filename):
    with open(filename, 'rb') as file:
        code, original_length = pickle.load(file)
        encoded_text = bitarray.bitarray()
        encoded_text.frombytes(file.read())
    return code, encoded_text, original_length

def load_text(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def average_code_length(frequencies, code):
    total_chars = sum(frequencies.values())
    avg_length = sum(len(code[char]) * freq for char, freq in frequencies.items()) / total_chars
    return avg_length

def compression_efficiency(original_text, encoded_text):
    original_size = len(original_text) * 8
    compressed_size = len(encoded_text)
    return original_size / compressed_size

filename = "norm_wiki_sample.txt"
data_folder = "dane/"
file_path = os.path.join(data_folder, filename)

if os.path.isfile(file_path):
    text = load_text(file_path)
    frequencies = {}
    for char in text:
        frequencies[char] = frequencies.get(char, 0) + 1

    huffman_tree = create_huffman_tree(frequencies)
    code = create_codes(huffman_tree)
    
    encoded_text = encode(text, code)
    
    save(code, encoded_text, os.path.join("encoded_data", filename + "_huffman.bin"), len(text))
    loaded_code, loaded_encoded_text, original_length = load(os.path.join("encoded_data", filename + "_huffman.bin"))
    
    decoded_text = decode(loaded_encoded_text, loaded_code, original_length)
    
    avg_length = average_code_length(frequencies, code)
    efficiency = compression_efficiency(text, encoded_text)

    print(f"Average Code Length: {avg_length}")
    print(f"Compression Efficiency: {efficiency}")
    print("Text is identical:", text == decoded_text)
else:
    print(f"File {filename} does not exist in the directory {data_folder}")
