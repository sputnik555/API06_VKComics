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


if __name__ == '__main__':

    load_dotenv()
    num = random.randint(1, get_current_comics_num())
    alt = download_comics('https://xkcd.com/{}/info.0.json'.format(num), "image.png")

    params = {
        'access_token': os.getenv('TOKEN'),
        'v': '5.131',
        'group_id': os.getenv('GROUP_ID'),
    }
    response = requests.get('https://api.vk.com/method/photos.getWallUploadServer', params)
    response.raise_for_status()

    upload_url = response.json()['response']['upload_url']

    with open('image.png', 'rb') as file:
        files = {'photo': file}
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        response = response.json()

    params['server'] = response['server']
    params['hash'] = response['hash']
    params['photo'] = response['photo']
    response = requests.post('https://api.vk.com/method/photos.saveWallPhoto', params=params)
    response.raise_for_status()

    post_params = {
        'access_token' : params['access_token'],
        'v': '5.131',
        'owner_id' : -207984001,
        'attachments' : 'photo{}_{}'.format(response['response'][0]['owner_id'],
                                            response['response'][0]['id']),
        'message' : alt

    }
    response = requests.post('https://api.vk.com/method/wall.post', params=post_params)
    response.raise_for_status()

    os.remove("image.png")