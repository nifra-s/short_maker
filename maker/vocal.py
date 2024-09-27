import asyncio
import json
import os
import random
from idlelib.iomenu import encoding

import edge_tts
from edge_tts import VoicesManager
from vtt_to_srt.vtt_to_srt import ConvertDirectories

async def gen_audio(scr, folder_name):
    global srt_files
    audio_files = []  # Array to store audio segments
    subtitle_files = []
    voices = await VoicesManager.create()
    voices = voices.find(Language="en")
    voice = random.choice(voices)["Name"]

    # Iterate over scenes and write the desired values to the CSV
    audio_sequence = 0

    communicate = edge_tts.Communicate(scr['title'], voice)
    sub_maker = edge_tts.SubMaker()
    audio_path = f"shorts\\{folder_name}\\vocal\\{str(audio_sequence)}.mp3"
    subtitle_path = f"shorts\\{folder_name}\\subtitle\\{str(audio_sequence)}.vtt"
    with open(audio_path, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                sub_maker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

    with open(subtitle_path, "w", encoding="utf-8") as file:
        file.write(sub_maker.generate_subs())
    audio_files.append(audio_path)
    subtitle_files.append(subtitle_path)

    audio_sequence += 1

    scenes = scr['scenes']
    for index, scene in enumerate(scenes):
        print(scene['narration'])
        communicate = edge_tts.Communicate(scene['narration'], voice)
        sub_maker = edge_tts.SubMaker()
        audio_path = f"shorts\\{folder_name}\\vocal\\{str(audio_sequence)}.mp3"
        subtitle_path = f"shorts\\{folder_name}\\subtitle\\{str(audio_sequence)}.vtt"
        with open(audio_path, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    sub_maker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

        with open(subtitle_path, "w", encoding="utf-8") as file:
            print(sub_maker.generate_subs())
            file.write(sub_maker.generate_subs())
        audio_files.append(audio_path)
        subtitle_files.append(subtitle_path)
        audio_sequence += 1
        convert_file = ConvertDirectories(f"shorts\\{folder_name}\\subtitle", False,"utf-8")
        convert_file.convert()
    return audio_files

# async def main() -> None:
#
#     # Open and read the JSON file
#     folder_name = 'shorts/1727346854.187433_mind-blowing_space_facts/subtitle'
#     # with open(f'shorts/{folder_name}/script.json', 'r') as file:
#     #     data = json.load(file)
#
#     merge_srt(folder_name)
#
# if __name__ == "__main__":
#     asyncio.run(main())