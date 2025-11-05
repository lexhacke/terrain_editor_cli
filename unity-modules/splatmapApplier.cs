using UnityEngine;

public class SplatmapApplier : MonoBehaviour
{
    public Terrain terrain;
    public Texture2D splatmap;  // Your RGBA splatmap texture
    public Texture2D[] textures; // Array to hold the textures for Grass, Rock, Snow, and Custom

    void Start()
    {
        ApplySplatmap();
    }

    void ApplySplatmap()
    {
        // Get the terrain's TerrainData
        TerrainData terrainData = terrain.terrainData;

        // Create a new splatmap (RGBA)
        float[,,] splatmapData = new float[terrainData.alphamapWidth, terrainData.alphamapHeight, 4];

        // Loop through each pixel in the splatmap and assign the corresponding texture
        for (int y = 0; y < terrainData.alphamapHeight; y++)
        {
            for (int x = 0; x < terrainData.alphamapWidth; x++)
            {
                // Get the color value of the splatmap at this pixel (RGBA)
                Color splatColor = splatmap.GetPixel(x, y);

                // Assign each texture based on the RGBA values (Grass, Rock, Snow, Custom)
                splatmapData[x, y, 0] = splatColor.r;  // Grass (Red channel)
                splatmapData[x, y, 1] = splatColor.g;  // Rock (Green channel)
                splatmapData[x, y, 2] = splatColor.b;  // Snow (Blue channel)
                splatmapData[x, y, 3] = splatColor.a;  // Custom (Alpha channel)
            }
        }

        // Set the terrain's splatmap data
        terrainData.SetAlphamaps(0, 0, splatmapData);
    }
}
