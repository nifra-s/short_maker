import asyncio
from datetime import datetime
import json

from maker import prompt, script, vocal, video, image, uploader

async def main() -> None:
    timestamp = str(datetime.now().timestamp())

    topic = prompt.get_topic('short_topics.xlsx')
    prom = prompt.get_prom(topic, 3)
    folder = prompt.write_prom(topic, timestamp, prom, 'master.csv')
    scr, search_keys, title = script.gen_script(prom, folder)
    images = image.scrap_image(search_keys, folder)

    audios, subtitles = await vocal.gen_vocal(scr, folder)
    video_path = video.create_video_with_audio(images, audios, folder)
    uploader.upload(path=video_path, title=title)
    # uploader.upload(path="shorts/1727672197.491431_facts_about_the_deepest_parts_of_the_earth/output.mp4", title="Deep Dive: 3 Facts About Earth's Deepest Depths")

if __name__ == "__main__":
    asyncio.run(main())
