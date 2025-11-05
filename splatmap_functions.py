import numpy as np
from IPython.display import clear_output
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from utils import noise2d, gaussian2d, radial_sigmoid
import numpy as np
from einops import rearrange
from biome_functions import *

def get_gradients(heightmap, smoothing_level=5):
    gradients = np.zeros(heightmap.shape)
    for y in range(1, heightmap.shape[0] - 1):
        for x in range(1, heightmap.shape[1] - 1):
            grad_x = (heightmap[y, x + 1] - heightmap[y, x - 1]) / 2.0
            grad_y = (heightmap[y + 1, x] - heightmap[y - 1, x]) / 2.0
            gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
            gradients[y, x] = gradient_magnitude
    return gaussian_filter(gradients, smoothing_level) # for smoothing

def get_splatmap(heightmap, rock_slope_threshold=0.035, snow_height=4.5):
    gradients = get_gradients(heightmap)
    splatmap = np.zeros((heightmap.shape[0], heightmap.shape[1], 4))

    # Grass: Low slope, and lower elevation areas
    grass_mask = (gradients < rock_slope_threshold) & (heightmap < snow_height)
    splatmap[:, :, 0] = gaussian_filter(grass_mask.astype(np.float32), 4)  # Red channel (Grass)

    # Rock: High slope areas
    rock_mask = gradients > rock_slope_threshold
    splatmap[:, :, 1] = gaussian_filter(rock_mask.astype(np.float32), 4)  # Green channel (Rock)

    # Snow: High elevation areas
    snow_mask = heightmap >= snow_height
    splatmap[:, :, 2] = gaussian_filter(snow_mask.astype(np.float32), 4)  # Blue channel (Snow)

    splatmap[:, :, 3] = 0.0  # Extra channel, for features later on
    return np.flip(rearrange(splatmap, "H W C -> W H C"), axis=0)

if __name__ == "__main__":
    fn_lookup = {
        'hills': hills_heightmap,
        'mountain': mountain_heightmap,
        'mesa': mesa_heightmap,
        'canyon': canyon_heightmap,
    }
    example_setup = [
        #{'biome': 'hills', 'center': (400, 400), 'radius': 280},
        {'biome': 'mountain', 'center': (230, 230), 'radius': 200},
        #{'biome': 'mesa', 'center': (500, 100), 'radius': 320},
        #{'biome': 'canyon', 'center': (100, 400), 'radius': 290}
    ]
    heightmap = base_heightmap()
    for object in example_setup:
        heightmap += fn_lookup[object['biome']](object['center'][0], object['center'][1], object['radius'])
    plt.imshow(heightmap)
    plt.colorbar()
    plt.show()
    def visualize_splatmap(splatmap):
        fig, ax = plt.subplots(1, 4, figsize=(15, 5))
        # Grass - Red channel
        ax[0].imshow(splatmap[:, :, 0], cmap='Greens')
        ax[0].set_title("Grass Mask (Red Channel)")
        ax[0].axis('off')
        # Rock - Green channel
        ax[1].imshow(splatmap[:, :, 1], cmap='Greens')
        ax[1].set_title("Rock Mask (Green Channel)")
        ax[1].axis('off')
        # Snow - Blue channel
        ax[2].imshow(splatmap[:, :, 2], cmap='Blues')
        ax[2].set_title("Snow Mask (Blue Channel)")
        ax[2].axis('off')
        # Alpha - Alpha channel (Optional, as a placeholder)
        ax[3].imshow(splatmap[:, :, 3], cmap='gray')
        ax[3].set_title("Alpha Mask (Alpha Channel)")
        ax[3].axis('off')
        plt.tight_layout()
        plt.show()
    splat = get_splatmap(heightmap)
    visualize_splatmap(splat)
    print(splat.shape)
    plt.imsave('splat.png', splat)