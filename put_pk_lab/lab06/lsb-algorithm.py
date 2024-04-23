def hide_message_in_pixels(pixels, message):
    # Konwertuj literę na binarny ciąg znaków
    binary_message = bin(message)[2:].zfill(len(pixels) * 3)

    # Osadź wiadomość w pikselach
    modified_pixels = []
    for i in range(len(pixels)):
        pixel = list(pixels[i])
        for j in range(3):
            pixel[j] = pixel[j] & ~1 | int(binary_message[i * 3 + j])
        modified_pixels.append(tuple(pixel))
    
    return modified_pixels

def reveal_message_from_pixels(pixels):
    # Odkryj ukrytą wiadomość z pikseli
    binary_message = ''
    for pixel in pixels:
        for channel in pixel:
            binary_message += str(channel & 1)
    
    # Konwertuj binarny ciąg znaków na liczbę całkowitą
    return int(binary_message, 2)

# Przykładowe piksele
pixels = [
    (43, 205, 24),
    (171, 204, 41),
    (28, 231, 90)
]

# Przykładowa wiadomość do ukrycia (43H = 01000011B)
message = 0b01000011

# Ukryj wiadomość w pikselach
modified_pixels = hide_message_in_pixels(pixels, message)
print("Zmodyfikowane piksele po ukryciu wiadomości:")
for pixel in modified_pixels:
    print(pixel)

# Odkryj wiadomość z pikseli
revealed_message = reveal_message_from_pixels(modified_pixels)
print("\nOdkryta wiadomość:", revealed_message)
