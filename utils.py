import numpy as np
from IPython.display import clear_output
import noise
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

normalize = lambda h : (h - h.min()) / (h.max() - h.min())

def gaussian2d(H, W, center_x, center_y, radius):
    X, Y = np.meshgrid(np.arange(W), np.arange(H))
    dx, dy = X - center_x, Y - center_y
    r2 = dx**2 + dy**2
    gauss = np.exp(-r2 / (2 * (radius**2)))
    return gauss

def radial_sigmoid(H, W, center_x, center_y, max_radius, steepness=10):
    """
    Generate a radial sigmoid function that decays around a center point in a circular manner.
    
    args:
        H (int): Height of the grid (heightmap)
        W (int): Width of the grid (heightmap)
        center_x (int): X-coordinate of the center of the radial decay
        center_y (int): Y-coordinate of the center of the radial decay
        max_radius (float): Maximum radius at which the decay reaches the asymptote
        steepness (float): Steepness of the sigmoid curve (higher = sharper decay)
    
    returns:
        np.ndarray: Heightmap with radial sigmoid decay
    """
    # Create a meshgrid of coordinates
    X, Y = np.meshgrid(np.arange(W), np.arange(H))
    
    # Calculate the squared distance from the center point
    dx, dy = X - center_x, Y - center_y
    r2 = dx**2 + dy**2
    
    # Scale the distance by the max radius
    r = np.sqrt(r2) / max_radius
    
    # Apply the sigmoid function: 1 / (1 + exp(-steepness * (r - 0.5)))
    # This ensures the value decays from 1 at the center to 0 at the max radius
    sigmoid = 1 / (1 + np.exp(steepness * (r - 0.5)))
    
    return sigmoid

def noise2d(oct, gain, lac, scale=1/200, freq=1, W=512, H=512, seed=None, return_octaves=False):
    """
    Create simplex noise with the following params
    args:
        oct (int) : number of octaves
        lac (float) : lacunarity
        scale (float) : scale, should be inversely proportional to H,W
        freq (float) : frequency, not touching this atm
        H (int) : Y dim of heightmap
        W (int) : X dim of heightmap
        seed (int) : should probably RNG this on init
        return_octaves (bool) : Set this to true if you want to manipulate particular octaves, otherwise sums over all octaves for all x,y
    """
    if seed is None:
        seed = np.random.randint(0,500)
    world = np.zeros((H, W, oct), dtype=np.float32)
    for y in range(H):
        for x in range(W):
            f = freq
            amp = 1/freq
            for i in range(oct):
                world[y][x][i] = amp * noise.snoise2(scale * x * f, scale * y * f,base=seed+i)
                amp *= gain
                f *= lac
    return world if return_octaves else world.sum(axis=-1)