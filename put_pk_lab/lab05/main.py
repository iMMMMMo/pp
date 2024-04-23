from PIL import Image
import random

def generate_shares(pixel_value):
    random_num = random.randint(0, 1)
    if pixel_value == 0:
        share1_val = [0, 255] if random_num == 0 else [255, 0]
        share2_val = [255, 0] if share1_val == [0, 255] else [0, 255]
    else:
        share1_val = [0, 255] if random_num == 0 else [255, 0]
        share2_val = share1_val[:]
    return share1_val, share2_val

def encrypt_image(image):
    share1_image = Image.new("1", (image.width * 2, image.height))
    share2_image = Image.new("1", (image.width * 2, image.height))

    for x in range(image.width):
        for y in range(image.height):
            pixel_value = image.getpixel((x, y))
            share1_pixels, share2_pixels = generate_shares(pixel_value)
            share1_image.putpixel((2 * x, y), share1_pixels[0])
            share1_image.putpixel((2 * x + 1, y), share1_pixels[1])
            share2_image.putpixel((2 * x, y), share2_pixels[0])
            share2_image.putpixel((2 * x + 1, y), share2_pixels[1])

    return share1_image, share2_image

def combine_shares(share1_image, share2_image):
    combined_image = Image.new("1", share1_image.size, color=0)

    for x in range(share1_image.width):
        for y in range(share1_image.height):
            share1_pixel_value = share1_image.getpixel((x, y))
            share2_pixel_value = share2_image.getpixel((x, y))
            combined_value = 255 if (share1_pixel_value == 255 and share2_pixel_value == 255) else 0
            combined_image.putpixel((x, y), combined_value)

    return combined_image

def main():
    original_image = Image.open("img2.png").convert("1")

    share1_image, share2_image = encrypt_image(original_image)

    combined_image = combine_shares(share1_image, share2_image)

    share1_image.save("share1.png")
    share2_image.save("share2.png")
    combined_image.save("combined.png")

if __name__ == "__main__":
    main()
