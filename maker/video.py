import asyncio
import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from moviepy.video.VideoClip import VideoClip, TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip


def count_images(image_files, number):
    count = 0
    for image_file in image_files:
        filename = os.path.basename(image_file)  # Get the file name from the path
        if filename.startswith(str(number)):  # Check if the filename starts with the number
            count += 1
    return count

def create_video_clip(audio_files, image_files, folder_name):
    output_temp = f"shorts\\{folder_name}\\temp"
    height = 1920
    width = 1080
    video_clips = []
    for idx, audio_path in enumerate(audio_files):
        image_clips = []
        # Load the audio file
        audio_clip = AudioFileClip(audio_path)
        audio_duration = round(audio_clip.duration, 3)

        count = count_images(image_files, idx)
        if count == 0:
            raise ValueError(f"No images found for audio file at index {idx}.")
        img_duration = round((audio_duration / count), 3)

        for img in range(count):
            # Load the image and create an ImageClip
            image_clip = ImageClip(image_files[idx * count + img])

            if img == 0:
                t_start, t_end = 0, round((img_duration * (img + 1)), 2)
            else:
                t_start, t_end = round((img_duration * img), 2), round((img_duration * (img + 1)), 2)

            # Get width and height of the image
            img_width, img_height = image_clip.size

            # Calculate aspect ratio
            img_aspect_ratio = img_width / img_height
            req_aspect_ratio = width / height

            # Resize the image based on aspect ratio
            if img_aspect_ratio > req_aspect_ratio:
                # Image is wider than required, fit height first, then crop width
                image_clip = image_clip.resize(height=height)
                # Calculate excess width to crop from both sides
                excess_width = (image_clip.w - width) / 2
                image_clip = image_clip.crop(x1=excess_width, x2=image_clip.w - excess_width)
            else:
                # Image is taller than required, fit width first, then crop height
                image_clip = image_clip.resize(width=width)
                # Calculate excess height to crop from top and bottom
                excess_height = (image_clip.h - height) / 2
                image_clip = image_clip.crop(y1=excess_height, y2=image_clip.h - excess_height)

            # Set the duration of the image to match the audio subclip duration
            image_clip = image_clip.set_duration(img_duration)

            # Set the audio for the image clip
            audio_subclip = audio_clip.subclip(t_start, t_end)
            image_clip = image_clip.set_audio(audio_subclip)

            image_clips.append(image_clip)

        # Concatenate all the image clips for this audio file
        final_clip = concatenate_videoclips(image_clips)

        generator = lambda txt: TextClip(txt, font='Arial-Black', fontsize=120, color='white', stroke_color='black', stroke_width=6)
        subtitle = f"shorts\\{folder_name}\\subtitle\\{idx}.srt"
        sub = SubtitlesClip(subtitle, generator)
        final_clip = CompositeVideoClip([final_clip, sub.set_position(('center',0.7), relative=True)])

        # final_clip.write_videofile(f"{output_temp}\\{idx}.mp4", codec="libx264", audio_codec="aac", fps=24)
        # video_clip = VideoFileClip(f"{output_temp}\\{idx}.mp4")
        video_clips.append(final_clip)

    return video_clips

def create_video_with_audio(image_files, audio_files, folder_name):
    output_video = f"shorts\\{folder_name}\\output.mp4"

    # Create individual video clips from the images and audio files
    video_clips = create_video_clip(audio_files, image_files, folder_name)

    # Concatenate the final video clips
    final_clips = concatenate_videoclips(video_clips)

    # Write the final video to the output file
    final_clips.write_videofile(output_video, codec="libx264", audio_codec="aac", fps=24)

    return output_video  # Return the final concatenated clip