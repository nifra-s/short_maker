import requests
import sys
import os

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
            for retry in range(0,2):
                image = requests.get(item['link'])
                # Check if the request was successful
                ext = item['fileFormat'].split("/")[1]
                if image.status_code == 200 and ext != "":
                    # Save the image to a file
                    image_path = f"shorts/{folder_name}/images/{idx}.{idy}.{ext}"
                    print(image_path)
                    with open(image_path, "wb") as file:
                        file.write(image.content)
                    file_size = os.path.getsize(image_path)
                    if file_size > 10000:
                        images.append(image_path)
                        idy = idy + 1
                        print(f"File downloaded completely.{file_size}")
                        break
                    else:
                        os.remove(image_path)
                        print(
                            f"File not downloaded completely. got {file_size} bytes.")
                else:
                    print(
                        f"File not downloaded completely. got error {image.status_code}")
            if idy > 3:
                break

    return images