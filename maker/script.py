from google.generativeai.types import HarmCategory, HarmBlockThreshold
from typing_extensions import TypedDict
import google.generativeai as genai
import json
import csv

# Define the schema for each scene
class Scene(TypedDict):
    title: str
    narration: str
    search_key: str
    image_prompt: str

# Define the schema for the entire structure
class Script(TypedDict):
    title: str
    scene: list[Scene]

def gen_script(prom, folder_name):
    API_KEY = "AIzaSyC3GNPHP-PP3w-U2OuvMuO5zucDb4gBEjo"

    genai.configure(api_key=API_KEY)

    prompt = prom + """
Use this JSON schema:
script = {'title': str, 'scenes': list[{'title': str, 'narration': str, 'image_prompt': str, 'search_key': str}]}
Return: script"""

    # Create the model
    generation_config = {
      "temperature": 2,
      "top_p": 0.95,
      "top_k": 64,
      "max_output_tokens": 8192,
      "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
              model_name="gemini-1.5-pro",
              generation_config = generation_config,
              safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
            )

    chat_session = model.start_chat()

    response = chat_session.send_message(prompt)

    script = json.loads(response.text)

    search_keys = save_script(script, folder_name)

    return script, search_keys, script["title"]

def save_script(script, folder_name):
    search_keys= [script['title']]
    file_path = 'shorts/' + folder_name + '/' + 'script.json'

    # Save data to a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(script, json_file, indent=4)
    keys_name = 'shorts/' + folder_name + '/' + 'keys.csv'
    # Open a CSV file for writing

    with open(keys_name, mode='w', newline='') as file:
        # Create a CSV writer
        writer = csv.writer(file)

        # Write the header (column names)
        writer.writerow(["image_prompt", "search_key"])
        scenes = script['scenes']
        # Iterate over scenes and write the desired values to the CSV
        for scene in scenes:
            writer.writerow([scene["image_prompt"], scene["search_key"]])
            search_keys.append(scene["search_key"])

    return search_keys