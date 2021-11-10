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
            date = str(datetime.utcfromtimestamp(date).strftime('%Y-%m-%d_%H_%M_%S'))
            likes_url_dict["file_name"] = likes
            likes_url_dict["sizes"] = items["sizes"][len(items["sizes"]) - 1]["type"]
            likes_url_dict["url"] = url_photo
            likes_url_dict["date"] = date
            json_list.append(likes_url_dict)
            likes_url_dict = {}
        return json_list


class YaUploader:
    def __init__(self, upload_list, token, id_vk):
        self.token = token
        self.upload_list = upload_list
        self.url = "https://cloud-api.yandex.net/v1/disk/resources/"
        self.headers = {'Authorization': self.token}
        self.id = id_vk

    def upload(self):
        check_list = self.get_list_name_photos()
        count_upload_photos = 0
        dir = requests.put(self.url, headers=self.headers, params={"path": self.id})
        if dir.status_code == 201 or dir.status_code == 409:
            if dir.status_code == 201:
                print(f"Папка с именем {self.id} созданна")
            else:
                print(f"Папка с именем {self.id} уже созданна")
            for dict in self.upload_list:
                buf = dict["file_name"] + ".jpeg"
                file_name = self.id + "/" + dict["file_name"] + ".jpeg"
                url_photo = dict["url"]
                params = {"path": file_name,
                          "url": url_photo}
                if not (buf in check_list):
                    response = requests.post(self.url + "upload", headers=self.headers, params=params)
                    if response.status_code != 202:
                        print(f"Произошла ошибка {response.status_code} при загрузке фото {file_name}")
                    else:
                        print(f"Фото {buf} загружено.")
                        count_upload_photos += 1
                else:
                    print(f"Файл с именем {buf} уже существует")
        else:
            print(f"ошибка {dir.status_code}")
        print(f"Загруженно фотографий: {count_upload_photos}")
        print("Завершенно")

    def get_list_name_photos(self):
        result_list = []
        response = requests.get(self.url + "files", headers=self.headers).json()
        for dict in response["items"]:
            name = dict["name"]
            result_list.append(name)
        return result_list


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
        dict['file_name'] += ".jpeg"
        del dict["date"]
        del dict["url"]
    with open("data_file.json", "w") as write_file:
        json.dump(buf, write_file, indent=5)
    return buf


id_vk = "552934290"
token_YD = "XXX"

Alex = VkUser(id_vk)
get_photos = Alex.get_photos(50)
work_dict = work_json_dict(get_photos)

uploader = YaUploader(work_dict, token_YD, id_vk)
uploader.upload()
uploader.get_list_name_photos()
print()
pprint(correct_json(work_dict))
