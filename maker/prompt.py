import os
import re

import  pandas as pd
import numpy as np

def get_prom(topic, facts_no):
    prom = f"""Write a script on {facts_no} {topic} for a short video. No need into in scene. don't include coma in image_prompt and search_key"""
    return prom

def get_topic(topic_path):
    topics_file = pd.read_excel(topic_path)
    topic = np.random.choice(topics_file['topics'])
    return topic

def write_prom(topic, timestamp, prom, master_file):
    folder_name = timestamp + "_" + _formate_topic(topic)
    data = {
        'timestamp': timestamp,
        'topic': topic,
        'prompt': prom,
        'folder_name': folder_name
    }
    df = pd.DataFrame([data])
    df.to_csv(master_file, mode='a', header=False, index=False)
    # Create the directory if it doesn't exist
    if not os.path.exists(f"shorts/{folder_name}"):
        os.makedirs(f"shorts/{folder_name}")
        os.makedirs(f"shorts/{folder_name}/images")
        os.makedirs(f"shorts/{folder_name}/vocal")
        os.makedirs(f"shorts/{folder_name}/temp")
        os.makedirs(f"shorts/{folder_name}/subtitle")
    return folder_name

def _formate_topic(input_string):

    # Replace unwanted characters with underscores or remove them entirely.
    pattern = r"[<>:\"/\\|?*\.]"
    modified_string = re.sub(pattern, "", input_string)

    # Replace spaces with underscores
    modified_string = modified_string.replace(" ", "_")

    # Remove leading and trailing underscores.
    modified_string = modified_string.strip("_")

    # Convert to lowercase
    modified_string = modified_string.lower()
    return modified_string