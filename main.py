import asyncio
import json

from maker import prompt, script, vocal, video, image
from datetime import datetime

async def main() -> None:
    timestamp = str(datetime.now().timestamp())

    topic = prompt.get_topic('short_topics.xlsx')
    prom = prompt.get_prom(topic, 3)
    folder = prompt.write_prom(topic, timestamp, prom, 'master.csv')
    scr, search_keys = script.gen_script(prom, folder)
    images = image.scrap_image(search_keys, folder)

    audios, subtitles = await vocal.gen_vocal(scr, folder)

if __name__ == "__main__":
    asyncio.run(main())
