import numpy as np
from IPython.display import clear_output
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from utils import noise2d, gaussian2d, radial_sigmoid

def base_heightmap(W=512, H=512):
    lower_octaves = noise2d(2, 0.6, 3, freq=0.8, scale=0.008, return_octaves=True)
    fine_detail = noise2d(6, 0.6, 3, freq=0.8, scale=0.05, return_octaves=True)[:, :, 2:] / 4
    perlin = 2*(lower_octaves.sum(axis=-1) + fine_detail.sum(axis=-1)) + 1
    return perlin / 10

def mountain_heightmap(center_x, center_y, radius, height=4, W=512, H=512):
    """
    Generate terrain with one localized mountain feature.
    """
    oct = 5
    gain = 0.3
    lac = 3.0
    scale = 1/200
    freq = 1
    amp = 1.0
    octaves = noise2d(oct, gain, lac, scale, freq, W, H, return_octaves=True)
    base_gauss = gaussian2d(octaves.shape[0], octaves.shape[1], center_x, center_y, radius*1.4)
    gauss = gaussian2d(octaves.shape[0], octaves.shape[1], center_x, center_y, radius)

    mountain = amp * (octaves[:,:,:2].sum(axis=-1) * gauss + height * base_gauss)
    heightmap = (base_gauss**0.25) * octaves[:,:,2:].sum(axis=-1) + mountain
    return heightmap

def hills_heightmap(center_x, center_y, radius, W=512, H=512):
    pdf = radial_sigmoid(H, W, center_x, center_y, radius*1.25, (np.random.rand()*3+8))
    octaves = noise2d(2, 0.4, 3, H=H, W=W, freq=0.8, scale=0.01, return_octaves=True)
    octaves[:,:,0] = gaussian_filter(octaves[:,:,0], 5)
    octaves[:,:,1] = gaussian_filter(abs(octaves[:,:,1]), 2)
    perlin = 0.5 * 2*octaves[:, :, :].sum(axis=-1) + 1
    return perlin * pdf

def mesa_heightmap(center_x, center_y, radius, H=512, W=512):
    octaves = 2*noise2d(oct=6, gain=0.2, lac=3, freq=1, scale=0.008, H=H, W=W, return_octaves=True) + 0.5
    octaves[:,:,0] = np.clip(2*(octaves[:,:,1] + octaves[:,:,0]), 0, 2.4 + np.random.rand() * 0.2)
    octaves[:,:,1] *= 0
    octaves[:,:,2:] = np.clip(octaves[:,:,2:], 0, np.random.rand() * 0.2)
    base = octaves.sum(axis=-1)
    return np.clip(base * radial_sigmoid(H, W, center_x, center_y, radius, 15), None, 5)

def canyon_heightmap(center_x, center_y, radius, H=512, W=512):
    return -mesa_heightmap(center_x, center_y, radius, H=H, W=W) / (np.random.rand() + 1.5)

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
    #plt.imshow(heightmap)
    #plt.colorbar()
    #plt.title(f"Heightmap (baseplate)")
    #plt.show()
    for object in example_setup:
        heightmap += fn_lookup[object['biome']](object['center'][0], object['center'][1], object['radius'])
        #plt.imshow(heightmap)
        #plt.colorbar()
        #plt.title(f"Heightmap with {object['biome']}")
        #plt.show()
        
    plt.imsave("example.png", heightmap)