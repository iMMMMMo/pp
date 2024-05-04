import matplotlib.pyplot as plt
from skimage.io import imread
import numpy as np

class Image:
    def __init__(self, path_to_image):
        self.image = imread(path_to_image, as_gray=True)
        self.height = self.image.shape[0]
        self.width = self.image.shape[1]
        self.size = min(self.height, self.width)
        self.center = tuple(x // 2 for x in self.image.shape)
        
        self.padded_image = self.get_image_with_padding()
        self.center_with_padding = tuple(x // 2 for x in self.padded_image.shape)
        self.size_with_padding = self.padded_image.shape[0]

    def get_size(self):
        return (self.height, self.width)

    def get_center(self):
        return self.center

    def get_image(self):
        return self.image

    def get_image_with_padding(self):
        outside_circle_radius = int(((self.height ** 2 + self.width ** 2) ** 0.5) // 2)
        width_to_add = outside_circle_radius - self.width // 2
        height_to_add = outside_circle_radius - self.height // 2

        width_to_add = max(0, width_to_add)
        height_to_add = max(0, height_to_add)

        image_with_padding = np.pad(self.image, ((height_to_add, height_to_add), (width_to_add, width_to_add)), mode='constant', constant_values=0)

        return image_with_padding

    def get_empty_image(self, shape):
        return np.zeros(shape)

    def plot(self):
        fig, ax = plt.subplots()
        ax.imshow(self.image, cmap="gray")
        plt.show()
