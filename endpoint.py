from biome_functions import *

class Master:
    def __init__(self, H, W):
        """
        Initialize terrain manager.
        Parameters:
            H: Height of the terrain grid
            W: Width of the terrain grid
        """
        self.biomes = []
        self.H, self.W = H, W
        self.fn_lookup = {
            'hills': hills_heightmap,
            'mountain': mountain_heightmap,
            'mesa': mesa_heightmap,
            'canyon': canyon_heightmap,
        }
        self.biomes.append({'matrix': base_heightmap() / 3})

    def context(self):
        """
        Generate human-readable summary of all added biomes.
        Returns:
            String describing each biome's type, center coordinates, and radius, in order of insertion
        """
        string = "The following is a list of biomes added to the heightmap in descending order by time of insertion\n"
        for i, item in enumerate(self.biomes):
            if i == 0:
                continue
            string += f"{i}. {item['biome']} at coordinates {item['center']} of radius {item['radius']}\n"
        return string

    def add(self, biome, center, radius):
        """
        Add a new biome layer to the terrain.
        Parameters:
            biome: Biome type name ('hills', 'mountain', 'mesa', 'canyon')
            center: Tuple (x, y) coordinates for biome center
            radius: Radius of influence for the biome
        """
        self.biomes.append({
                'matrix': self.fn_lookup[biome](center[0], center[1], radius),
                'biome': biome,
                'center': center,
                'radius': radius,
            })

    def compile(self):
        """
        Combine all biome layers into final heightmap.
        Returns:
            Numpy array of combined terrain heights
        """
        terrain = self.biomes[0]['matrix'].copy()
        for item in self.biomes:
            terrain += item['matrix']
        return terrain + terrain.min()

    def remove(self, index):
        """Remove a biome layer by its index.

        Parameters:
            index: Index of biome to remove (0 is base heightmap)
        """
        self.biomes.pop(index)

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    master = Master(512, 512)
    example_setup = [
        {'biome': 'hills', 'center': (400, 400), 'radius': 280},
        {'biome': 'mountain', 'center': (30, 30), 'radius': 200},
        {'biome': 'mesa', 'center': (500, 100), 'radius': 320},
        {'biome': 'canyon', 'center': (100, 400), 'radius': 290}
    ]
    for item in example_setup:
        master.add(item['biome'], item['center'], item['radius'])
        plt.imsave('temp.png',master.compile())
        print([item['biome'] for item in master.biomes[1:]])
        print(master.context())
    master.remove(3)
    plt.imsave('rm.png',master.compile())
    print([item['biome'] for item in master.biomes[1:]])
    print(master.context())