import asyncio
import json

from maker import prompt, script, vocal, video, image
from datetime import datetime

async def main() -> None:
    # timestamp = str(datetime.now().timestamp())
    #
    # topic = prompt.get_topic('short_topics.xlsx')
    # prom = prompt.get_prom(topic, 3)
    # folder = prompt.write_prom(topic, timestamp, prom, 'master.csv')
    # scr, search_keys = script.gen_script(prom, folder)
    # images = image.scrap_image(search_keys, folder)
    #
    # vocals = await vocal.gen_audio(scr, folder)
    # print(vocals)
    # print(subtitles)
    # print(images)
    # print(folder)
    folder = "1727366287.642287_rare_diseases_you_might_not_have_heard_of"
    images = ['shorts/1727366287.642287_rare_diseases_you_might_not_have_heard_of/images/0.0.jpeg', 'shorts/1727366287.642287_rare_diseases_you_might_not_have_heard_of/images/0.1.jpeg', 'shorts/1727366287.642287_rare_diseases_you_might_not_have_heard_of/images/0.2.jpeg', 'shorts/1727366287.642287_rare_diseases_you_might_not_have_heard_of/images/0.3.jpeg', 'shorts/1727366287.642287_rare_diseases_you_might_not_have_heard_of/images/1.0.jpeg', 'shorts/1727366287.642287_rare_diseases_you_might_not_have_heard_of/images/1.1.jpeg', 'shorts/1727366287.642287_rare_diseases_you_might_not_have_heard_of/images/1.2.jpeg', 'shorts/1727366287.642287_rare_diseases_you_might_not_have_heard_of/images/1.3.jpeg', 'shorts/1727366287.642287_rare_diseases_you_might_not_have_heard_of/images/2.0.png', 'shorts/1727366287.642287_rare_diseases_you_might_not_have_heard_of/images/2.1.jpeg', 'shorts/1727366287.642287_rare_diseases_you_might_not_have_heard_of/images/2.2.jpeg', 'shorts/1727366287.642287_rare_diseases_you_might_not_have_heard_of/images/2.3.jpeg', 'shorts/1727366287.642287_rare_diseases_you_might_not_have_heard_of/images/3.0.jpeg', 'shorts/1727366287.642287_rare_diseases_you_might_not_have_heard_of/images/3.1.png', 'shorts/1727366287.642287_rare_diseases_you_might_not_have_heard_of/images/3.2.jpeg', 'shorts/1727366287.642287_rare_diseases_you_might_not_have_heard_of/images/3.3.jpeg']
    vocals = ['shorts\\1727366287.642287_rare_diseases_you_might_not_have_heard_of\\vocal\\0.mp3', 'shorts\\1727366287.642287_rare_diseases_you_might_not_have_heard_of\\vocal\\1.mp3', 'shorts\\1727366287.642287_rare_diseases_you_might_not_have_heard_of\\vocal\\2.mp3', 'shorts\\1727366287.642287_rare_diseases_you_might_not_have_heard_of\\vocal\\3.mp3']
    # Open and read the JSON file
    with open(f'shorts/{folder}/script.json', 'r') as file:
        scr = json.load(file)

    video_path = video.create_video_with_audio(images, vocals, folder)


if __name__ == "__main__":
    asyncio.run(main())