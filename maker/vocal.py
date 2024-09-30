import random

import edge_tts
import srt
from edge_tts import VoicesManager
from vtt_to_srt.vtt_to_srt import ConvertFile
from tqdm.asyncio import tqdm as tqdm_asyncio


def _convert_srt_to_single_word_lines(_input_file):
    with open(_input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Parse the subtitles using srt package
    subs = list(srt.parse(content))
    new_subs = []
    counter = 1

    previous_end_time = None  # To track the end time of the previous subtitle

    # Iterate over each subtitle
    for sub in subs:
        start_time = sub.start
        end_time = sub.end

        # Preserve the gap between previous subtitle and current one
        if previous_end_time and start_time > previous_end_time:
            gap_duration = start_time - previous_end_time
            gap_sub = srt.Subtitle(
                index=counter,
                start=previous_end_time,
                end=start_time,
                content=""  # No content for gaps
            )
            new_subs.append(gap_sub)
            counter += 1

        # Split the subtitle text into words
        words = sub.content.split()

        # Calculate time duration per word
        total_duration = end_time - start_time
        word_duration = total_duration / len(words)

        # Create a new subtitle for each word
        for i, word in enumerate(words):
            word_start_time = start_time + i * word_duration
            word_end_time = word_start_time + word_duration

            # Create a new subtitle entry for each word
            new_sub = srt.Subtitle(
                index=counter,
                start=word_start_time,
                end=word_end_time,
                content=word
            )
            new_subs.append(new_sub)
            counter += 1

        # Update previous_end_time for the next subtitle
        previous_end_time = end_time

    # Write the new subtitles to a file
    with open(_input_file, 'w', encoding='utf-8') as out_file:
        out_file.write(srt.compose(new_subs))

async def _gen_clip(folder_name, audio_sequence, voice, text):
    communicate = edge_tts.Communicate(text, voice)
    sub_maker = edge_tts.SubMaker()
    audio_path = f"shorts\\{folder_name}\\vocal\\{str(audio_sequence)}.mp3"
    vtt_path = f"shorts\\{folder_name}\\subtitle\\{str(audio_sequence)}.vtt"
    srt_path = f"shorts\\{folder_name}\\subtitle\\{str(audio_sequence)}.srt"
    
    # Initialize communication to get the estimated audio length
    chunks = communicate.stream()
    
    # Estimate number of chunks by getting text length (as a rough measure)
    total_chunks = len(text) // 5  # Assuming around 5 characters per chunk for estimation
    
    # Progress bar setup
    with open(audio_path, "wb") as file:
        async for chunk in tqdm_asyncio(chunks, total=total_chunks, desc="Generating Audio", ncols=100, unit="chunk"):
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                sub_maker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

    # Writing the subtitle files
    with open(vtt_path, "w", encoding="utf-8") as file:
        file.write(sub_maker.generate_subs())
    
    # Convert VTT to SRT
    convert_file = ConvertFile(vtt_path, "utf-8")
    convert_file.convert()

    # Ensure the SRT file is formatted properly
    _convert_srt_to_single_word_lines(srt_path)

    print("Subtitle Created")
    return audio_path, srt_path

async def gen_vocal(scr, folder_name):
    audio_files = []  # Array to store audio segments
    subtitle_files = []

    voices = await VoicesManager.create()
    voices = voices.find(Language="en")
    voice = random.choice(voices)["Name"]

    # Iterate over scenes and write the desired values to the CSV
    audio_sequence = 0

    audio_path, srt_path = await _gen_clip(folder_name, audio_sequence, voice, scr['title'])
    audio_files.append(audio_path)
    subtitle_files.append(srt_path)
    audio_sequence += 1

    scenes = scr['scenes']
    for index, scene in enumerate(scenes):
        audio_path, srt_path = await _gen_clip(folder_name, audio_sequence, voice, scene['narration'])
        audio_files.append(audio_path)
        subtitle_files.append(srt_path)
        audio_sequence += 1

    return audio_files, subtitle_files