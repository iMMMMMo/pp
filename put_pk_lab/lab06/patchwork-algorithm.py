from PIL import Image
import numpy as np

def embed_watermark(image, secret_key, n):
    d = 5

    np.random.seed(secret_key)
    
    watermark_pixels = np.random.randint(0, image.size[0], size=(n, 2))
    watermark_pixels[:, 1] = np.random.randint(0, image.size[1], size=n)
    
    pixels = image.load()
    
    for pixel in watermark_pixels:
        Ai = tuple(pixel)
        Bi = (np.random.randint(0, image.size[0]), np.random.randint(0, image.size[1])) # szerokość i wysokość
        
        pixels[Ai] = tuple([min(255, channel + d) for channel in pixels[Ai]])
        pixels[Bi] = tuple([max(0, channel - d) for channel in pixels[Bi]])
    

    sum_diff = np.sum(np.diff(np.array(image)))
    S_n = 2 * d * n + sum_diff
    
    return image, S_n

def detect_watermark(image, secret_key, n, expected_Sn):
    d = 5
    
    np.random.seed(secret_key)
    
    watermark_pixels = np.random.randint(0, image.size[0], size=(n, 2))
    watermark_pixels[:, 1] = np.random.randint(0, image.size[1], size=n)
    
    pixels = image.load()
    
    for pixel in watermark_pixels:
        Ai = tuple(pixel)
        Bi = (np.random.randint(0, image.size[0]), np.random.randint(0, image.size[1]))
        
        pixels[Ai] = tuple([max(0, channel - d) for channel in pixels[Ai]])
        pixels[Bi] = tuple([min(255, channel + d) for channel in pixels[Bi]])
    
    sum_diff = np.sum(np.diff(np.array(image)))
    Sn = sum_diff
    
    print(f"Wartość Sn po osadzeniu znaku wodnego {expected_Sn}.")
    print(f"Wartość Sn po detekcji znaku wodnego {Sn}.")
    return abs(Sn - expected_Sn) < 500

image_path = "example.png"
secret_key = 31
n = 10

image = Image.open(image_path)

watermarked_image, S_n = embed_watermark(image, secret_key, n)

watermarked_image.save("watermarked_example.png")

watermark_detected = detect_watermark(watermarked_image, secret_key, n, S_n)

if watermark_detected:
    print("Znak wodny został poprawnie wykryty.")
else:
    print("Nie wykryto znaku wodnego.")