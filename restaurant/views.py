from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from .models import Restaurant
from bearbites.models import Account
from menu.models import Menu, MenuItem


# Create your views here.

def browseLocationView(request):

    if request.method == 'POST':
        target = Restaurant()
        target.zipQuery.clear()
        search = request.POST.get('search')
       
        try:
            int(search)
        except ValueError:
            if len(search) ==0:
                restaurants = target.view_AllRestaurants()    
                context = {'response': "",'restaurants':restaurants}
                return render(request,'locations.html',context)
            else:
                
                restaurants = target.searchStreetAddressOrName(search)    
                context = {'response': "",'restaurants':restaurants}
                return render(request,'locations.html',context)
        
        if len(int(search))== 5:
            menuIt = MenuItem()
            restaurants = target.searchZipCode(int(search))
            RestaurantName ="Carl's JR"
            menuItems = menuIt.viewMenu(1)
            if 'name' in request.session:
                userInfo = request.session["name"]
            else:
                userInfo = ""
            context = {'response': "",'restaurants':restaurants,'menuitems':menuItems,'RestaurantName':RestaurantName,'username':userInfo}
            return render(request,'locations.html',context)
      

    else:
        target = Restaurant()
        menuIt = MenuItem()
        restaurants = target.view_AllRestaurants()
        RestaurantName ="Carl's JR"
        menuItems = menuIt.viewMenu(1)
        if 'name' in request.session:
            userInfo = request.session["name"]
        else:
            userInfo = ""
        context = {'response': "",'restaurants':restaurants,'menuitems':menuItems,'RestaurantName':RestaurantName,'username':userInfo}
        return render(request,'locations.html',context)
