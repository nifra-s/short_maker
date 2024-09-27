import xml.etree.ElementTree as ET

from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})


def create_video_template():
    # output_video = f"shorts\\{folder_name}\\output.xml"
    template = "video_templates/video_.xml"

    root = ET.parse(template).getroot()

    # Iterate over images and corresponding audio files
    count = 0
    for element in root.findall(".//clipitem"):

        name = element.find(".//file/name").text
        print(name)
        count = count + 1
        print(count)

create_video_template()


