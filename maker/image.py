import requests
import sys
import os

def download_file(output_path, link, retry = 1):
    count = 0
    while count <= retry:
        print("retrying")
        count = count + 1
        image = requests.get(link)
        # Check if the request was successful

        if image.status_code == 200:
            # Save the image to a file
            with open(output_path, "wb") as file:
                file.write(image.content)
            file_size = os.path.getsize(output_path)
            if file_size > 10000:
                return output_path
            else:
                os.remove(output_path)
    return 0

def get_img_url():
    pass

def get_extension(link):
    image_extensions = ["jpg", "jpeg", "png", "webp"]
    ext = link.split(".")[-1].split("?")[0]
    if ext in image_extensions:
        return ext
    return None


def scrap_image(search_keys, folder_name):
    images = []
    print(search_keys)
    for idx, query in enumerate(search_keys):

        # API_KEY_PEXEL = "SKZHXhZQZZRMeLroAI9gjy6pCcVtrq6IfnZjEV26cfFjm88OElLJIjan"

        API_KEY = 'AIzaSyDCGayjwRzVMjCtkLOW6K6_NTFW3WS0uCU'
        SEARCH_ENGINE_ID = '01433498d097f47f4'
    
        url = 'https://www.googleapis.com/customsearch/v1'

        params = {
            'q': query,
            'key': API_KEY,
            'cx': SEARCH_ENGINE_ID,
            'searchType': 'image',
            'imgSize': 'xxlarge',
            'safe': 'off',
            'imgColorType': 'color',
            'imgType': 'photo',
        }

        response = requests.get(url, params=params)
        results = response.json()['items']
        print(results)

        idy = 0
        for item in results:
            ext = get_extension(item["link"])
            print(ext)
            output_path = f"shorts/{folder_name}/images/{idx}.{idy}.{ext}"
            image_path = download_file(output_path, item['link'], 2)
            if image_path:
                images.append(image_path)
                idy = idy + 1
                print(f"File downloaded completely")
            if idy > 3:
                break

    return images