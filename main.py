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
        return json_list


# В ключ file_name кладем правильное значение, убираем дубли.
# Возвращает инфомацию с url и file_name
def work_json_dict(list_of_dictionaries):
    for dict_check in list_of_dictionaries:
        for dict in list_of_dictionaries:
            if (dict_check["file_name"] == dict["file_name"]) and (dict_check["url"] != dict["url"]):
                dict_check["file_name"] = dict_check["file_name"] + "_" + "(" + dict_check["date"] + ")"
                dict["file_name"] = dict["file_name"] + "_" + "(" + dict["date"] + ")"
    return list_of_dictionaries


# Возвращает итоговый json и создает его
def correct_json(json_dict):
    buf = json_dict
    for dict in buf:
        del dict["date"]
        del dict["url"]
    with open("data_file.json", "w") as write_file:
        json.dump(buf, write_file, indent=5)
    return buf


Alex = VkUser("552934290")

pprint(correct_json(work_json_dict(Alex.get_photos(50))))
print()
pprint(work_json_dict(Alex.get_photos(50)))
