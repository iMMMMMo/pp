from Crypto.Cipher import AES
import time
import matplotlib.pyplot as plt

def load_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

def save_file(file_path, data):
    with open(file_path, 'wb') as f:
        f.write(data)

def encrypt_data(data, key, mode):
    cipher = AES.new(key, mode)
    return cipher.encrypt(data)

def decrypt_data(data, key, mode):
    cipher = AES.new(key, mode)
    return cipher.decrypt(data)

def measure_time(data, key, mode):
    start_time = time.time()
    encrypted_data = encrypt_data(data, key, mode)
    encryption_time = time.time() - start_time

    start_time = time.time()
    decrypted_data = decrypt_data(encrypted_data, key, mode)
    decryption_time = time.time() - start_time

    return encryption_time, decryption_time


def main():
    key = b'0123456789abcdef'  # Klucz 128-bitowy (16 bajtów)
    file_names = ["plaintext_100MB.txt", "plaintext_200MB.txt", "plaintext_300MB.txt"]

    modes = {
        "ECB": AES.MODE_ECB,
        "CBC": AES.MODE_CBC,
        "OFB": AES.MODE_OFB,
        "CFB": AES.MODE_CFB,
        "CTR": AES.MODE_CTR
    }

    encryption_times = {mode_name: [] for mode_name in modes.keys()}
    decryption_times = {mode_name: [] for mode_name in modes.keys()}

    for mode_name, mode in modes.items():
        print(f"Tryb: {mode_name}")
        for file_name in file_names:
            data = load_file(file_name)
            encryption_time, decryption_time = measure_time(data, key, mode)
            encryption_times[mode_name].append(encryption_time)
            decryption_times[mode_name].append(decryption_time)
            print(f"Rozmiar danych: {len(data) / (1024 * 1024)} MB")
            print(f"Czas szyfrowania: {encryption_time:.6f} sekund")
            print(f"Czas deszyfrowania: {decryption_time:.6f} sekund")
            print()

    plt.figure(figsize=(10, 5))
    for mode_name in modes.keys():
        plt.plot(file_names, encryption_times[mode_name], label=f"{mode_name} szyfrowanie")

    plt.xlabel('Rozmiar pliku (MB)')
    plt.ylabel('Czas (sekundy)')
    plt.title('Czasy szyfrowania w różnych trybach pracy szyfrów blokowych')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))
    for mode_name in modes.keys():
        plt.plot(file_names, decryption_times[mode_name], label=f"{mode_name} deszyfrowanie")

    plt.xlabel('Rozmiar pliku (MB)')
    plt.ylabel('Czas (sekundy)')
    plt.title('Czasy deszyfrowania w różnych trybach pracy szyfrów blokowych')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
