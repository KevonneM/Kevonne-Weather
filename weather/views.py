from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm

from django.conf import settings
import os
from decouple import config

import json
with open('/etc/config.json') as config_file:
    config = json.load(config_file)

# Create your views here.

def index(request):
    """The home page for the weather app."""
    return render(request, 'weather/index.html')

def search(request):
    """The search page fpr the weather app."""
    url = config.get("WEATHER_URL")

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        
        # Prevents duplicate cities from being submitted.
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world.'
            else:
                err_msg = 'City already exists in the database!'
                

        if err_msg:
            message = err_msg
            message_class = 'alert alert-danger'
        else:
            message = 'City added successfully'
            message_class = 'alert alert-success'

    form = CityForm()

    cities = City.objects.all()

    weather_data = []
       
    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'].title(),
            'icon': r['weather'][0]['icon']
        }
        
        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form, 'message': message}

    return render(request, 'weather/search.html', context)

def delete_city(request, city_name):
    """This is used to delete individual cities."""

    City.objects.get(name=city_name).delete()

    return redirect('weather:search')

def delete_everything(request):
    """This is used to delete all the cities in the database"""

    cities = City.objects.all()
    for city in cities:
        City.objects.get(name=city).delete()

    return redirect('weather:search')
