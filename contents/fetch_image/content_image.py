# import config
import os
import requests
def content_image(query):

    # IMAGE_API_KEY = config.PIXEL_API_KEY
    IMAGE_API_KEY = os.environ['PIXEL_API_KEY']
    url = "https://api.pexels.com/v1/search"
    querystring = { 'query' : query , "per_page" : 1, 'size' : 4, 'orientation': 'landscape'}

    headers = {
        'Authorization' : IMAGE_API_KEY
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        photos = data.get('photos')
        img_url = photos[0]['src']['large2x']
    
    return img_url