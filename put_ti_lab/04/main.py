import bitarray
import pickle
import os

def create(frequencies):
    code = {}
    byte_size = 6
    i = 0
    for char in sorted(frequencies.keys()):
        code[char] = format(i, 'b').zfill(byte_size)
        i += 1
    return code, byte_size

def encode(text, code):
    encoded_text = bitarray.bitarray()
    for char in text:
        encoded_text.extend(code[char])
    return encoded_text

def decode(encoded_text, code):
    reversed_code = {v: k for k, v in code.items()}
    decoded_text = ""
    current_code = ""
    for bit in encoded_text:
        current_code += '1' if bit else '0'
        if current_code in reversed_code:
            decoded_text += reversed_code[current_code]
            current_code = ""
    return decoded_text

def save(code, encoded_text, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as file:
        pickle.dump(code, file)
        encoded_text.tofile(file)

def load(filename):
    with open(filename, 'rb') as file:
        code = pickle.load(file)
        encoded_text = bitarray.bitarray()
        encoded_text.fromfile(file)
    return code, encoded_text

def load_text(filename):
    with open(filename, 'r') as file:
        text = file.read()
    return text

data_folder = "dane/"
files = os.listdir(data_folder)

print("Are original and decoded text identical?")
for file in files:
    text = load_text(os.path.join(data_folder, file))
    frequencies = {}
    for char in text:
        frequencies[char] = frequencies.get(char, 0) + 1

    print(f"File {file}:")
    
    code, byte_size = create(frequencies)
    encoded_text = encode(text, code)
    save(code, encoded_text, os.path.join("encoded_data", file + f"_byte_size_{byte_size}.bin"))
    loaded_code, loaded_encoded_text = load(os.path.join("encoded_data", file + f"_byte_size_{byte_size}.bin"))
    decoded_text = decode(loaded_encoded_text, loaded_code)
    print(f"Byte Size: {byte_size}:", text == decoded_text, end="")
    if not text == decoded_text:
        print(f"\nCompression ratio: {len(text) * 8 / len(encoded_text)}")
    else:
        print()
