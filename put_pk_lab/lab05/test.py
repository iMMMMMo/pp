from PIL import Image
import random

def split_image(image_path, output_path1, output_path2):
    original_image = Image.open(image_path).convert("L")

    width, height = original_image.size
    share1 = Image.new("L", (width, height))
    share2 = Image.new("L", (width, height))

    for x in range(width):
        for y in range(height):
            pixel = original_image.getpixel((x, y))
            share1_pixel = random.randint(0, 255)
            share2_pixel = pixel ^ share1_pixel
            share1.putpixel((x, y), share1_pixel)
            share2.putpixel((x, y), share2_pixel)

    share1.save(output_path1)
    share2.save(output_path2)

def combine_shares(share_path1, share_path2, output_path):
    share1 = Image.open(share_path1)
    share2 = Image.open(share_path2)
    width, height = share1.size
    combined_image = Image.new("L", (width, height))

    for x in range(width):
        for y in range(height):
            pixel1 = share1.getpixel((x, y))
            pixel2 = share2.getpixel((x, y))
            combined_pixel = pixel1 ^ pixel2
            combined_image.putpixel((x, y), combined_pixel)

    combined_image.save(output_path)


image_path = "img.png"
output_path1 = "share1.png"
output_path2 = "share2.png"
split_image(image_path, output_path1, output_path2)


share_path1 = "share1.png"
share_path2 = "share2.png"
output_path = "combined_image.png"
combine_shares(share_path1, share_path2, output_path)
