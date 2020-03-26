from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from restaurant.models import Restaurant
from bearbites.models import Account
from .models import MenuItem
# Create your views here.

def openMenuView(request):
    if request.method == 'POST':
        restaurant = Restaurant()
        name = request.POST.get("name")
        restaurant.set_restaurantName(name)
        location = request.POST.get("location")
        restaurant.fetchLocation(location)
        
