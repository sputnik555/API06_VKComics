import requests
from dotenv import load_dotenv
import os
import random


def get_comics_image_url(num):
    response = requests.get('https://xkcd.com/{}/info.0.json'.format(num))
    response.raise_for_status()
    response = response.json()
    return response['img'], response['alt']


def download_file(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def get_current_comics_num():
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    return response.json()['num']


def download_random_comics_image(filename):
    num = random.randint(1, get_current_comics_num())
    url, alt = get_comics_image_url(num)
    download_file(url, filename)
    return alt


def get_vk_upload_url(token, group_id):
    params = {
        'access_token': token,
        'v': '5.131',
        'group_id': group_id,
    }

    response = requests.get('https://api.vk.com/method/photos.getWallUploadServer', params)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def upload_vk_image(filename, upload_url):
    with open(filename, 'rb') as file:
        files = {'photo': file}
        response = requests.post(upload_url, files=files)

    response.raise_for_status()
    response = response.json()

    return response['server'], response['hash'], response['photo']


def save_vk_wall_photo(token, group_id, server, hash, photo):
    params = {
        'access_token': token,
        'v': '5.131',
        'group_id': group_id,
        'server': server,
        'hash': hash,
        'photo': photo
    }

    response = requests.post('https://api.vk.com/method/photos.saveWallPhoto', params=params)
    response.raise_for_status()
    response = response.json()

    return response['response'][0]['owner_id'], response['response'][0]['id']


def post_vk_wall(token, group_id, owner_id, photo_id, alt):
    post_params = {
        'access_token': token,
        'v': '5.131',
        'owner_id': '-{}'.format(group_id),
        'attachments': 'photo{}_{}'.format(owner_id, photo_id),
        'message': alt

    }

    response = requests.post('https://api.vk.com/method/wall.post', params=post_params)
    response.raise_for_status()


if __name__ == '__main__':

    load_dotenv()
    token = os.getenv('VK_TOKEN')
    group_id = os.getenv('VK_GROUP_ID')
    filename = os.getenv('TEMPFILENAME')

    try:
        alt = download_random_comics_image(filename)
        upload_url = get_vk_upload_url(token, group_id)
        server, hash, photo = upload_vk_image(filename, upload_url)
        owner_id, photo_id = save_vk_wall_photo(token, group_id, server, hash, photo)
        post_vk_wall(token, group_id, owner_id, photo_id, alt)
    finally:
        os.remove(filename)
