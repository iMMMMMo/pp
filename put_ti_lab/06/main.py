import bitarray
import pickle
import os

def create(text, max_dict_size=None):
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    return dictionary, dict_size, max_dict_size

def encode(text, dictionary):
    dict_size = dictionary[1]
    max_dict_size = dictionary[2]
    dictionary = dictionary[0]

    string = ""
    compressed_data = []

    for symbol in text:
        string_plus_symbol = string + symbol
        if string_plus_symbol in dictionary:
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            if max_dict_size is None or len(dictionary) < max_dict_size:
                dictionary[string_plus_symbol] = dict_size
                dict_size += 1
            string = symbol

    if string:
        compressed_data.append(dictionary[string])

    bit_stream = bitarray.bitarray()
    for data in compressed_data:
        bit_stream.frombytes(data.to_bytes(3, byteorder='big')) 

    return bit_stream

def decode(bit_stream, max_dict_size=None):
    from io import StringIO
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}

    compressed_data = []
    for i in range(0, len(bit_stream), 24):
        bits = bit_stream[i:i+24]
        compressed_data.append(int.from_bytes(bits.tobytes(), byteorder='big'))
    
    string = chr(compressed_data.pop(0))
    result = StringIO()
    result.write(string)

    for code in compressed_data:
        if code in dictionary:
            entry = dictionary[code]
        elif code == dict_size:
            entry = string + string[0]
        else:
            raise ValueError('Bad compressed k: %s' % code)
        result.write(entry)

        if max_dict_size is None or len(dictionary) < max_dict_size:
            dictionary[dict_size] = string + entry[0]
            dict_size += 1

        string = entry

    return result.getvalue()

def save(bit_stream, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as file:
        pickle.dump(bit_stream, file)

def load(filename):
    with open(filename, 'rb') as file:
        bit_stream = pickle.load(file)
    return bit_stream

def load_text(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def load_binary(filename):
    with open(filename, 'rb') as file:
        data = file.read()
    return data

data_folder = "dane/"
files = os.listdir(data_folder)

for file in files:
    if file.endswith('.txt'):
        text = load_text(os.path.join(data_folder, file))
    else:
        text = load_binary(os.path.join(data_folder, file)).decode('latin1')

    print(f"Plik {file}:")

    dictionary = create(text)
    bit_stream = encode(text, dictionary)
    save(bit_stream, os.path.join("encoded_data", file + "_compressed.bin"))
    loaded_bit_stream = load(os.path.join("encoded_data", file + "_compressed.bin"))
    decoded_text = decode(loaded_bit_stream, dictionary[2])
    print("Bez ograniczenia słownika:", text == decoded_text)

    for max_dict_size in [2**12, 2**18]:
        dictionary = create(text, max_dict_size)
        bit_stream = encode(text, dictionary)
        save(bit_stream, os.path.join(f"encoded_data/{file}_compressed_{max_dict_size}.bin"))
        loaded_bit_stream = load(os.path.join(f"encoded_data/{file}_compressed_{max_dict_size}.bin"))
        decoded_text = decode(loaded_bit_stream, max_dict_size)
        print(f"Z ograniczeniem słownika do {max_dict_size} elementów:", text == decoded_text)
