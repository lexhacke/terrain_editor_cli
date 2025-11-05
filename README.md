# TerrainLex

A procedural terrain generation system with natural language control, designed for Unity integration. Generate realistic heightmaps and splatmaps using AI-powered commands.

## Features

- **Natural Language Interface**: Describe terrain modifications in plain English using GPT-5
- **Multiple Biome Types**: Mountains, hills, mesas, and canyons with realistic noise-based generation
- **Automatic Splatmap Generation**: Texture maps based on slope and elevation (grass, rock, snow)
- **Unity Integration**: Export-ready heightmaps and splatmaps for Unity terrain
- **Procedural Generation**: Perlin noise-based terrain with customizable parameters

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd TerrainProject
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root:
```
OPENAI_KEY=your_openai_api_key_here
```

## Usage

### CLI Mode

Run the interactive terrain generator:
```bash
python cli.py
```

Follow the prompts:
1. Enter the path where you want terrain/splatmap images saved
2. Describe your terrain in natural language

Example commands:
- "Add a mountain to the left"
- "Add 3 mountains on the bottom right"
- "Add a mesa in the top right"
- "Remove the second mountain"

The system will generate:
- `terrain.png` - Heightmap for Unity terrain
- `splat.png` - Splatmap for texture painting (R=grass, G=rock, B=snow)

### Programmatic Usage

```python
from endpoint import Master
import matplotlib.pyplot as plt

# Initialize terrain manager
master = Master(512, 512)

# Add biomes manually
master.add('mountain', center=(230, 230), radius=200)
master.add('hills', center=(400, 400), radius=280)
master.add('canyon', center=(100, 400), radius=290)

# Compile and save
compiled = master.compile()
plt.imsave('terrain.png', compiled['heights'])
plt.imsave('splat.png', compiled['splat'])
```

## Project Structure

```
TerrainProject/
├── cli.py                    # Natural language CLI interface
├── endpoint.py               # Master terrain manager
├── biome_functions.py        # Biome generation functions
├── splatmap_functions.py     # Texture map generation
├── utils.py                  # Noise and mathematical utilities
├── requirements.txt          # Python dependencies
├── TerrainLex.unitypackage  # Unity integration package
└── .env                      # API keys (not committed)
```

## Biome Types

### Mountain
High-elevation peaks with realistic noise-based features. Best for dramatic terrain.

### Hills
Rolling terrain with gentle slopes. Good for transitional areas.

### Mesa
Flat-topped plateaus with steep sides. Creates distinctive landmarks.

### Canyon
Inverted mesa terrain creating valleys and crevices.

## Splatmap Channels

Generated splatmaps use RGB channels for texture assignment:
- **Red Channel**: Grass (low slope, low elevation)
- **Green Channel**: Rock (high slope areas)
- **Blue Channel**: Snow (high elevation areas, >4.5 units)
- **Alpha Channel**: Reserved for future features

## Configuration

Terrain parameters can be adjusted in the respective functions:

**Terrain Size**: Modify `H` and `W` parameters in `Master(H, W)`
- Default: 512x512

**Splatmap Thresholds** (in `splatmap_functions.py`):
- `rock_slope_threshold`: 0.035 (adjust for more/less rock)
- `snow_height`: 4.5 (adjust snow line elevation)

## Unity Integration

1. Import `TerrainLex.unitypackage` into your Unity project
2. Generate terrain and splatmap using the CLI or programmatic interface
3. Import generated PNG files into Unity
4. Apply heightmap to terrain
5. Use splatmap with terrain layers (assign grass/rock/snow textures to R/G/B channels)

## Requirements

- Python 3.7+
- OpenAI API key (for CLI mode)
- See `requirements.txt` for full dependency list

## License

See LICENSE file for details.

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
