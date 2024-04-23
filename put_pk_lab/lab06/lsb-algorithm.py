from PIL import Image

def encode_message(image_path, message, num_bits):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    
    binary_message = bin(message)[2:].zfill(8)
    
    pixels_needed = len(binary_message) // num_bits
    if len(binary_message) % 3 != 0:
        pixels_needed += 1
    
    for i in range(pixels_needed):
        pixel = pixels[i]
        modified_pixel = list(pixel)
        
        print(f"Piksel {i+1}. ", end = "")
        print(f"({' '.join([bin(channel)[2:].zfill(8) for channel in pixel])}) - ", end= "")
        
        for j in range(num_bits):
            if len(binary_message) > 0:
                bit = binary_message[0]
                modified_pixel[j] = modify_bit(pixel[j], bit)
                binary_message = binary_message[1:]
        
        pixels[i] = tuple(modified_pixel)
        
        print(f"({' '.join([bin(channel)[2:].zfill(8) for channel in pixels[i]])})")


    print("Zaszyfrowana wiadomość:", bin(message)[2:].zfill(8))

    img.putdata(pixels)
    img.save("encoded_image.png")

def modify_bit(value, bit):
    mask = 0b11111110
    if bit == "1":
        return value | 1
    else:
        return value & mask

image_path = "example.png"

message = 0b0100100101010100010101111111

num_bits = 3
encode_message(image_path, message, num_bits)
