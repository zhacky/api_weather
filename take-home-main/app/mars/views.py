import os
import requests

from django.shortcuts import render


# Create your views here.
def mars_index(request):
    API_KEY = os.environ.get('NASA_API_KEY')
    mars_url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={api_key}'

    if request.method == 'POST':
        data_src_type = None
        if request.POST['url_src'] is not None:
            mars_data = fetch_mars_photos_from_url(api_key=API_KEY, mars_api_url=mars_url)
            context = {
                'mars_data': mars_data
            }
            return render(request, 'mars.html', context)

        print("No images")
        return render(request, 'mars.html')
    else:
        return render(request, 'mars.html')


def fetch_mars_photos_from_url(api_key, mars_api_url, max=100):
    if max >= 100:
        max = 100
    response = requests.get(mars_api_url.format(api_key=api_key)).json()
    mars_data = []
    for i, mars in enumerate(response['photos'], max):
        mars_data.append({
            'title': mars['camera']['full_name'],
            'image': mars['img_src'],
            'max': max
        })

    return mars_data
