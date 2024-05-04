from math import radians
import numpy as np
import matplotlib.pyplot as plt
from algorithms import normalize_array, bresenham

class CTScanner:
    def __init__(self, center, radius, range_angle, devices_count, scan_count, image, up_to_angle):
        self.center = center
        self.radius = radius
        self.range_angle = radians(range_angle)
        self.devices_count = devices_count
        self.scan_count = scan_count
        self.measurement_angles = np.linspace(0, 180, self.scan_count)
        self.image = image
        self.result_image = np.zeros(image.shape)
        self.normalization_matrix = np.zeros(image.shape)
        self.sinogram = None
        self.transposed_sinogram = None
        self.up_to_angle = up_to_angle
        self.measurement_angles = self.measurement_angles[self.measurement_angles <= self.up_to_angle]

    def calculate_sinogram_data(self):
        results = np.zeros((self.scan_count, self.devices_count))

        for i, angle in enumerate(self.measurement_angles):
            results[i] = self.radon_transform(angle)

        results = normalize_array(results)
        
        self.sinogram = results
        self.transposed_sinogram = np.transpose(results)
    
    def radon_transform(self, angle):
        emitters_coords = self.get_emitters_coords(angle)
        detectors_coords = self.get_detectors_coords(angle)
        lines = self.get_lines_between_devices(emitters_coords, detectors_coords)

        result = normalize_array(np.array([np.sum((self.image[tuple(line)])) for line in lines]))

        return result

    def calculate_result_data(self):
        for _, angle in enumerate(self.measurement_angles):
            self.inverse_radon_transform(angle)
            
        self.normalization_matrix[self.normalization_matrix == 0] = 1
        self.result_image = normalize_array(self.result_image / self.normalization_matrix)

    def inverse_radon_transform(self, angle):
        print(angle)
        emitters_coords = self.get_emitters_coords(angle)
        detectors_coords = self.get_detectors_coords(angle)
        lines = self.get_lines_between_devices(emitters_coords, detectors_coords)

        for i, line in enumerate(lines):
            for point in np.transpose(line):
                if int(angle / (180 / self.scan_count)) < self.scan_count:
                    self.result_image[point[0], point[1]] += np.transpose(self.transposed_sinogram)[int(angle / (180 / self.scan_count)), i]
                    self.normalization_matrix[point[0], point[1]] += 1
                    
    def get_emitters_coords(self, angle):
        return self.get_devices_coords(angle)

    def get_detectors_coords(self, angle):
        return self.get_devices_coords(angle + 180)[::-1]

    def get_devices_coords(self, angle):
        devices_angles = np.linspace(0, self.range_angle, self.devices_count) + radians(angle)
        center_x, center_y = self.center
        devices_x = (self.radius * np.cos(devices_angles) - center_x).astype(int)
        devices_y = (self.radius * np.sin(devices_angles) - center_y).astype(int)
        devices_coords = list(zip(devices_x, devices_y))

        return devices_coords

    def get_lines_between_devices(self, emitters_coords, detectors_coords):
        lines = [list(bresenham(emitter_coords, detector_coords)) for emitter_coords, detector_coords in zip(emitters_coords, detectors_coords)]
        return lines
    
    def plot_sinogram(self):
        plt.imshow(self.transposed_sinogram, cmap="gray", aspect="auto")
        plt.title("Sinogram")
        plt.show()


    def plot_result(self):
        plt.figure()
        plt.imshow(self.result_image, cmap="gray")
        plt.show()

    def get_image(self):
        inside_circle_radius = int(self.image.shape[0] // 2)
        size_to_subtract = int(inside_circle_radius // np.sqrt(2))
        original_x = int(self.image.shape[0] // 2 - size_to_subtract)
        original_y = int(self.image.shape[0] // 2 - size_to_subtract)

        image_without_padding = self.image[original_x:original_x + 2 * size_to_subtract, original_y:original_y + 2 * size_to_subtract]

        return image_without_padding

    def get_result_image(self):
        inside_circle_radius = int(self.result_image.shape[0] // 2)
        size_to_subtract = int(inside_circle_radius // np.sqrt(2))
        original_x = int(self.result_image.shape[0] // 2 - size_to_subtract)
        original_y = int(self.result_image.shape[0] // 2 - size_to_subtract)

        image_without_padding = self.result_image[original_x:original_x + 2 * size_to_subtract, original_y:original_y + 2 * size_to_subtract]

        return image_without_padding

    def get_sinogram_history(self):
        print(self.sinogram_history.shape)
        return self.sinogram_history

    def get_result_history(self):
        print(self.result_image_history.shape)
        return self.result_image_history

    def get_transposed_sinogram(self):
        return self.transposed_sinogram
