import numpy as np
import matplotlib.pyplot as plt
import pydicom
import os
from scipy.ndimage import convolve
import tkinter as tk
from tkinter import ttk

def read_dicom_image(filepath):
    ds = pydicom.dcmread(filepath)
    return ds.pixel_array


def bresenham_line(x0, y0, x1, y1):
    # Implementacja algorytmu Bresenhama
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while x0 != x1 or y0 != y1:
        points.append((x0, y0))
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    points.append((x1, y1))
    return points

def radon_transform(image, steps, n, l):
    # Implementacja transformaty Radona
    height, width = image.shape
    sinogram = np.zeros((steps, n))

    for i in range(steps):
        theta = np.deg2rad(i / steps * 180.0)
        for j in range(n):
            alpha = np.deg2rad((j / n - 0.5) * l)
            x0 = int(width / 2 + (width / 2 + n / 2) * np.cos(theta - alpha))
            y0 = int(height / 2 + (height / 2 + n / 2) * np.sin(theta - alpha))
            x1 = int(width / 2 + (width / 2 + n / 2) * np.cos(theta + alpha))
            y1 = int(height / 2 + (height / 2 + n / 2) * np.sin(theta + alpha))
            line = bresenham_line(x0, y0, x1, y1)
            projection = np.sum(image[line[:, 1], line[:, 0]]) / len(line)
            sinogram[i, j] = projection

    return sinogram

def inverse_radon_transform(sinogram, steps, n, l):
    # Implementacja odwrotnej transformaty Radona
    height = sinogram.shape[0]
    width = sinogram.shape[1]
    image = np.zeros((height, height))

    for i in range(steps):
        theta = np.deg2rad(i / steps * 180.0)
        for j in range(n):
            alpha = np.deg2rad((j / n - 0.5) * l)
            x0 = int(width / 2 + (width / 2 + n / 2) * np.cos(theta - alpha))
            y0 = int(height / 2 + (height / 2 + n / 2) * np.sin(theta - alpha))
            x1 = int(width / 2 + (width / 2 + n / 2) * np.cos(theta + alpha))
            y1 = int(height / 2 + (height / 2 + n / 2) * np.sin(theta + alpha))
            line = bresenham_line(x0, y0, x1, y1)
            image[line[:, 1], line[:, 0]] += sinogram[i, j]

    return image

def backprojection(sinogram, images):
    height, width = images[0].shape
    reconstructed_image = np.zeros((height, width))

    for i in range(sinogram.shape[0]):
        theta = np.deg2rad(i / sinogram.shape[0] * 180.0)
        for j in range(sinogram.shape[1]):
            alpha = np.deg2rad((j / sinogram.shape[1] - 0.5) * l)
            x0 = int(width / 2 + (width / 2 + n / 2) * np.cos(theta - alpha))
            y0 = int(height / 2 + (height / 2 + n / 2) * np.sin(theta - alpha))
            x1 = int(width / 2 + (width / 2 + n / 2) * np.cos(theta + alpha))
            y1 = int(height / 2 + (height / 2 + n / 2) * np.sin(theta + alpha))
            line = bresenham_line(x0, y0, x1, y1)
            reconstructed_image[line[:, 1], line[:, 0]] += sinogram[i, j]

    return reconstructed_image


def filter_sinogram(sinogram):
    # Implementacja filtrowania sinogramu
    kernel = np.ones(21) / 21  # Prosty filtr uśredniający
    filtered_sinogram = np.zeros_like(sinogram)
    for i in range(sinogram.shape[0]):
        filtered_sinogram[i, :] = convolve(sinogram[i, :], kernel, mode='constant')
    return filtered_sinogram

def update():
    step = int(step_slider.get())
    detectors = int(detectors_slider.get())
    span = float(span_slider.get())
    
    selected_image = dicom_images[0]  # Wybierz pierwszy obraz z listy
    sinogram = radon_transform(selected_image, steps=step, n=detectors, l=span)
    filtered_sinogram = filter_sinogram(sinogram)
    reconstructed_image = inverse_radon_transform(filtered_sinogram, steps=step, n=detectors, l=span)
    
    # Wyświetlenie obrazu oryginalnego
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.imshow(selected_image, cmap='gray')
    plt.title('Original DICOM Image')

    # Wyświetlenie zrekonstruowanego obrazu
    plt.subplot(1, 2, 2)
    plt.imshow(reconstructed_image, cmap='gray')
    plt.title('Reconstructed Image')
    plt.show()

# Tworzenie głównego okna GUI
root = tk.Tk()
root.title("Tomograf Komputerowy")

# Wczytanie obrazów DICOM
dicom_folder = 'dicoms'
dicom_images = read_dicom_image("dicoms/Paski2.dcm")

# Utworzenie suwaków
step_label = tk.Label(root, text="Krok α")
step_slider = tk.Scale(root, from_=1, to=360, orient="horizontal")
step_slider.set(180)
detectors_label = tk.Label(root, text="Liczba detektorów")
detectors_slider = tk.Scale(root, from_=1, to=200, orient="horizontal")
detectors_slider.set(100)
span_label = tk.Label(root, text="Rozpiętość układu emiter/detektor")
span_slider = tk.Scale(root, from_=0.1, to=2.0, resolution=0.1, orient="horizontal")
span_slider.set(1.0)

# Przycisk aktualizacji
update_button = tk.Button(root, text="Aktualizuj", command=update)

# Umieszczenie elementów w oknie
step_label.pack()
step_slider.pack()
detectors_label.pack()
detectors_slider.pack()
span_label.pack()
span_slider.pack()
update_button.pack()

# Uruchomienie pętli głównej GUI
root.mainloop()
