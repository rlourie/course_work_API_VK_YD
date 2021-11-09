import requests
import json
from pprint import pprint
from datetime import datetime


class VkUser:
    def __init__(self, id):
        self.url = "https://api.vk.com/method/"
        self.token = "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008"
        self.id = id
        self.params = {"access_token": self.token,
                       "v": "5.131",
                       "owner_id": self.id
                       }

    def get_photos(self, count):
        json_list = []
        likes_url_dict = {}
        get_photos_params = {
            "album_id": "profile",
            "extended": "1",
            "count": count,
            "photo_sizes": "1"
        }
        get_photos_url = self.url + "photos.get"
        req = requests.get(get_photos_url, params={**self.params, **get_photos_params}).json()
        for items in req["response"]["items"]:
            likes = str(items["likes"]["count"])
            url_photo = items["sizes"][len(items["sizes"]) - 1]["url"]
            date = items["date"]
            date = str(datetime.utcfromtimestamp(date).strftime('%Y-%m-%d_%H:%M:%S'))
            likes_url_dict["file_name"] = likes
            likes_url_dict["sizes"] = items["sizes"][len(items["sizes"]) - 1]["type"]
            likes_url_dict["url"] = url_photo
            likes_url_dict["date"] = date
            json_list.append(likes_url_dict)
            likes_url_dict = {}
        pprint(json_list)
        with open("data_file.json", "w") as write_file:
            json.dump(json_list, write_file)
            print(write_file)
        return 0


Alex = VkUser("552934290")

pprint(Alex.get_photos(50))
