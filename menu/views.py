from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from restaurant.models import Restaurant
from bearbites.models import Account
from .models import Menu, MenuItem
# Create your views here.

def openMenuView(request):
    if request.method == 'POST':
        restaurant = Restaurant()
        name = request.POST.get("name")
        restaurant.set_restaurantName(name)
        location = request.POST.get("location")
        resID = restaurant.fetchLocation(location) #Get the RestaurantID for target Location
        menu = Menu()
        menuID = menu.queryMenu(resID)
        menuItem = MenuItem()
        context = menuItem.queryMenu(menuID) #Query ALl Menu Items as a Dictionary
        return render(request,'menu.html',context)
    else:
        context = {'response':""}
        return render(request,'menu.html',context)
