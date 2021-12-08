import requests
from dotenv import load_dotenv
import os
import random


def download_comics(url, filename):

    response = requests.get(url)
    response.raise_for_status()
    response = response.json()

    image_response = requests.get(response['img'])
    image_response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(image_response.content)

    return response['alt']


def get_current_comics_num():

    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    return response.json()['num']


def download_random_comics_image(filename):

    num = random.randint(1, get_current_comics_num())
    return download_comics('https://xkcd.com/{}/info.0.json'.format(num), filename)


def get_vk_upload_url(token, group_id):

    params = {
        'access_token': token,
        'v': '5.131',
        'group_id': group_id,
    }

    response = requests.get('https://api.vk.com/method/photos.getWallUploadServer', params)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def vk_upload_image(filename, upload_url, token, group_id):

    with open(filename, 'rb') as file:
        files = {'photo': file}
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        response = response.json()

    params = {
        'access_token': token,
        'v': '5.131',
        'group_id': group_id,
        'server': response['server'],
        'hash': response['hash'],
        'photo': response['photo']
    }

    response = requests.post('https://api.vk.com/method/photos.saveWallPhoto', params=params)
    response.raise_for_status()
    response = response.json()

    return response['response'][0]['owner_id'], response['response'][0]['id']


def vk_wall_post(token, owner_id, id, alt):

    post_params = {
        'access_token': token,
        'v': '5.131',
        'owner_id': owner_id,
        'attachments': 'photo{}_{}'.format(owner_id, id),
        'message': alt

    }

    response = requests.post('https://api.vk.com/method/wall.post', params=post_params)
    response.raise_for_status()


if __name__ == '__main__':

    load_dotenv()
    token = os.getenv('TOKEN')
    group_id = os.getenv('GROUP_ID')

    alt = download_random_comics_image('image.png')
    upload_url = get_vk_upload_url(token, group_id)
    owner_id, id = vk_upload_image('image.png', upload_url, token, group_id)
    vk_wall_post(token, owner_id, id, alt)

    os.remove("image.png")
