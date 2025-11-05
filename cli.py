from dotenv import load_dotenv
from endpoint import Master
from openai import OpenAI
import json
import os
import matplotlib.pyplot as plt

load_dotenv()

class GPTWrapper:
  def __init__(self):
    self.gpt = OpenAI(api_key=os.environ['OPENAI_KEY'])

  def generate_gpt(self, prompt):
    assert "system" in prompt and "user" in prompt, "Prompt must contain 'system' and 'user' keys"
    response = self.gpt.responses.create(
      model="gpt-5-mini",
      input=[
        {
          "role": "developer",
          "content": [
            {
              "type": "input_text",
              "text": prompt['system']
            }
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "type": "input_text",
              "text": prompt['user']
            }
          ]
        }
      ],
      text={
        "format": {
          "type": "text"
        },
        "verbosity": "medium"
      },
      reasoning={
        "effort": "medium"
      },
      store=True,
      include=[
        "reasoning.encrypted_content",
        "web_search_call.action.sources"
      ]
      )
    return response.output_text

agent = GPTWrapper()

system_prompt = lambda list_of_biomes : f"""
Task:
You are given a natural language command to modify terrain by either adding or removing biomes. Based on the command, you must generate a structured JSON output that represents the operation.
Your task is to output the operation and the parameters required to modify the terrain. You need to interpret commands that involve adding or deleting biomes and output the corresponding JSON structure.
Expected Operations:
Add Operation: When the command involves adding new biomes to the terrain, the system should provide the biome type, coordinates (center), and radius.
Delete Operation: When the command involves removing a specific biome, the system should output the 1-based index of the biome to be deleted.
Format:
{{
  "operation": "add" | "delete",
  "args": [  // List of biomes to add (for add operation)
    {{
      "biome": "mountain" | "hills" | "canyon" | "mesa",
      "center": [int, int],
      "radius": int
    }},
    ...
  ],
  "index": int  // 1-based index of biome to delete (for delete operation)
}}

Example Commands:
Command:
"Add a mountain to the left, 3 mountains on the bottom right, a mesa in the top right."
Output:
{{
  "operation": "add",
  "args": [
    {{"biome": "mountain", "center": [100, 250], "radius": 180}},
    {{"biome": "mountain", "center": [400, 450], "radius": 90}},
    {{"biome": "mountain", "center": [450, 450], "radius": 90}},
    {{"biome": "mountain", "center": [500, 450], "radius": 90}},
    {{"biome": "mesa", "center": [400, 100], "radius": 60}}
  ]
}}

Command: "Remove the second mountain."
Output:
{{
  "operation": "delete",
  "index": 2
}}

Command: "Make the terrain bigger, add a desert biome."
Output:
{{
  "operation": "add",
  "args": [
    {{"biome": "desert", "center": [250, 250], "radius": 100}}
  ]
}}

Biomes Already in the Environment:
The current list of biomes in the environment (before any changes) should be referenced in the command interpretation. When performing the delete operation, you will need to track the indices of the biomes, and use them in subsequent commands.
{list_of_biomes}

Natural Language Parsing:

Add Operation:
When the command involves adding features, break down the position (left, right, top-right, bottom-left, etc.) and return the respective indices in "center" and biome type (mountain, mesa, etc.). For example:

"Add a mountain to the left" → Place a mountain with a center near [100, 250] on the left side and a reasonable size.

"3 mountains on the bottom right" → Place 3 mountain biomes near the bottom-right section of the grid with a reasonable radius considering the current environment.

Delete Operation:
When the command involves removing a feature, identify the number of the biome to be deleted as described. If it says 1. Mountain then return "index":1 do not zero-index your return value.
"""

if __name__ == "__main__":
    master = Master(512, 512)
    print("Lex's Terrain CLI Ready :)")
    print("Enter the path where you want your splats and terrains saved: ")
    path = input()
    print("Describe your ideal terrain")
    while True:
        response = agent.generate_gpt({'user': input(), 'system': system_prompt(master.context())})
        response = json.loads(response)
        if response['operation'] == 'add':
           for arg in response['args']:
              master.add(arg['biome'], arg['center'], arg['radius'])
        elif response['operation'] == 'delete':
            master.remove(int(response['index']))
        print(master.context())
        obj = master.compile()
        plt.imsave(path+'\\'+"terrain.png", obj['heights'])
        plt.imsave(path+'\\'+"splat.png", obj['splat'])
        print(f"Saved heightmap to {path}"+"\\"+"terrain.png")
        print(f"Saved splatmap to {path}"+"\\"+"splat.png")