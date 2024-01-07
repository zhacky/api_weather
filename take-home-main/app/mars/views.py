import os
import requests

from django.shortcuts import render
from django.db import transaction
from mars.models import Photo


# Create your views here.
def mars_index(request):
    API_KEY = os.environ.get('NASA_API_KEY')
    mars_url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={api_key}&page={page}'

    if request.method == 'POST':
        if 'url_src' in request.POST:
            page = int(request.POST['page'])
            mars_data = fetch_mars_photos_from_url(api_key=API_KEY, mars_api_url=mars_url, page=page)
            context = {
                'mars_data': mars_data
            }
            return render(request, 'mars.html', context)

        elif 'db_save' in request.POST:
            page = int(request.POST['page'])
            count = save_to_db(api_key=API_KEY, mars_api_url=mars_url, page=page)
            return render(request, 'mars.html', count)

        elif 'db_src' in request.POST:
            page = int(request.POST['page'])
            mars_data = fetch_mars_photos_from_db(page)
            context = {
                'mars_data': mars_data
            }
            return render(request, 'mars.html', context)


        print("No images loaded.")
        return render(request, 'mars.html')
    else:
        return render(request, 'mars.html')


def fetch_mars_photos_from_url(api_key, mars_api_url, page):
    response = requests.get(mars_api_url.format(api_key=api_key, page=page)).json()
    mars_data = []
    for i, mars in enumerate(response['photos']):
        mars_data.append({
            'title': mars['camera']['full_name'],
            'image': mars['img_src'],
            'page': page
        })

    return mars_data


@transaction.atomic()
def save_to_db(api_key, mars_api_url, page):
    response = requests.get(mars_api_url.format(api_key=api_key, page=page)).json()
    mars_data = []
    for i, mars in enumerate(response['photos']):
        photo = Photo()
        photo.id = mars['id']
        photo.title = mars['camera']['full_name']
        photo.image = mars['img_src']
        mars_data.append(photo)

    objs = Photo.images.bulk_create(mars_data)
    context = {
        'count': len(objs)
    }
    return context


def fetch_mars_photos_from_db(page):
    limit = page*25
    photoSet = Photo.images.all()[:limit]
    mars_data = []
    for i, mars in enumerate(list(photoSet)):
        mars_data.append({
            'title': mars.title,
            'image': mars.image,
            'page': page
        })

    return mars_data
