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
        
        if 'name' in request.session:
                userInfo = request.session["name"]
        else:
            userInfo = ""
        try:
            int(search)
        except ValueError:

            if len(search) ==0:
                restaurants = target.view_AllRestaurants()    
                context = {'response': "",'restaurants':restaurants,'username':userInfo}
                return render(request,'locations.html',context)
            else:
                restaurants = target.searchStreetAddressOrName(search)    
                context = {'response': "",'restaurants':restaurants,'username':userInfo}
                return render(request,'locations.html',context)
        
        if len(search)== 5:
            
            restaurants = target.searchZipCode(int(search))
            
            context = {'response': "",'restaurants':restaurants,'username':userInfo}
            return render(request,'locations.html',context)
      

    else:
        target = Restaurant()
        restaurants = target.view_AllRestaurants()
        
        if 'name' in request.session:
            userInfo = request.session["name"]
        else:
            userInfo = ""
        context = {'response': "",'restaurants':restaurants,'username':userInfo}
        return render(request,'locations.html',context)

def searchRestaurant(request):
   
    menuIt = MenuItem()
    restaurantID = request.GET['pk']
    print(str(restaurantID))
    menuIt.set_restaurantID(int(restaurantID))
    menuItems = menuIt.viewItems()
    restaurantInfo =  menuIt.viewRestaurant()
    
    con = {'menuitems':menuItems,'restaurantInfo':restaurantInfo}
    return render(request,'menu.html',con)