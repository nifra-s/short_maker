import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
import json
import csv

from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

def _get_subtitle(script, audio_path):
    idy = 0
    subtitle = []
    time = 0.0
    # Load the audio file
    audio_clip = AudioFileClip(audio_path)
    audio_duration = round(audio_clip.duration / 4, 3)
    time += round(audio_duration, 3)
    print(audio_duration)
    if idy == 0:
        words = script['title'].split(" ")
        print(words)
    else:
        words = script['scenes'][idy - 1]['narration'].split(" ")
        print(words)
    delay = round(audio_duration / len(words), 2)

    for idx, word in enumerate(words):
        subtitle_line = ((round((time + (idx * delay)), 2), round(((idx * delay) + delay + time), 2)), word)
        subtitle.append(subtitle_line)

    return subtitle

def create_video_clip(audio_files, image_files):
    video_clips = []
    for idx, audio_path in enumerate(audio_files):
        audio_clip = AudioFileClip(audio_path)
        print(audio_clip.duration)
        audio_duration = round(audio_clip.duration / 4, 3)
        print(audio_duration)

        time1, time2, time3, time4 = round((audio_duration * 1), 2), round((audio_duration * 2), 2), round(
            (audio_duration * 3), 2), round((audio_duration * 4), 2)
        print(f"{time1}-{time2}-{time3}-{time4}")

        audio_clip1 = audio_clip.subclip(0, time1)
        audio_clip2 = audio_clip.subclip(time1, time2)
        audio_clip3 = audio_clip.subclip(time2, time3)
        audio_clip4 = audio_clip.subclip(time3, time4)

        # final_text = concatenate_videoclips(subtitle)

        # Load the image and create an ImageClip
        image_clip1 = ImageClip(image_files[idy * 4 + 0])
        image_clip2 = ImageClip(image_files[idy * 4 + 1])
        image_clip3 = ImageClip(image_files[idy * 4 + 2])
        image_clip4 = ImageClip(image_files[idy * 4 + 3])

        # Set the duration of the image to match the audio duration
        image_clip1 = image_clip1.set_duration(audio_duration)
        image_clip2 = image_clip2.set_duration(audio_duration)
        image_clip3 = image_clip3.set_duration(audio_duration)
        image_clip4 = image_clip4.set_duration(audio_duration)

        # resize all clip
        image_clip1 = image_clip1.resize(height=1920)
        image_clip1 = image_clip1.crop(y_center=960, height=1920, x1=540, x2=1620)
        image_clip2 = image_clip2.resize(height=1920)
        image_clip2 = image_clip2.crop(y_center=960, height=1920, x1=540, x2=1620)
        image_clip3 = image_clip3.resize(height=1920)
        image_clip3 = image_clip3.crop(y_center=960, height=1920, x1=540, x2=1620)
        image_clip4 = image_clip4.resize(height=1920)
        image_clip4 = image_clip4.crop(y_center=960, height=1920, x1=540, x2=1620)

        # Set the audio for the image clip
        image_clip1 = image_clip1.set_audio(audio_clip1)
        image_clip2 = image_clip2.set_audio(audio_clip2)
        image_clip3 = image_clip3.set_audio(audio_clip3)
        image_clip4 = image_clip4.set_audio(audio_clip4)

        video_clips.append(image_clip1)
        video_clips.append(image_clip2)
        video_clips.append(image_clip3)
        video_clips.append(image_clip4)

        idy = idy + 1

    return video_clips



def create_video_with_audio(image_files, audio_files, folder_name, script):
    screensize = (720, 460)
    output_video = f"shorts\\{folder_name}\\output.mp4"

    # Iterate over images and corresponding audio files
    video_clips = create_video_clip(audio_files, image_files)

    generator = lambda txt: TextClip(txt, font='Arial', fontsize=100, color='white')
    # lrs = _get_subtitle(script, audio_files)
    # subtitles = SubtitlesClip(lrs, generator)

    final_video = concatenate_videoclips(video_clips)

    # final_video = CompositeVideoClip([final_video, subtitles.set_position(("center", "center"))])
    # final_video = CompositeVideoClip(final_video)

    # # Write the output video file
    final_video.write_videofile(output_video, fps=24)

    return final_video