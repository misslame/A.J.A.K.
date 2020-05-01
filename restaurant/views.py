from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from .models import Restaurant
from bearbites.models import Account
from menu.models import Menu, MenuItem
from bearbites.views import get_userinfo


# Create your views here.

def browseLocationView(request):
    context = get_userinfo(request)
    if request.method == 'POST':
        target = Restaurant()
        target.zipQuery.clear()
        search = request.POST.get('search')
        searchName = request.POST.get('searchName')
        try:
            int(search)
            int(searchName)
        except ValueError:

            if len(search) ==0 and len(searchName)== 0:
                restaurants = target.view_AllRestaurants()
            else:

                if len(search) ==0 and len(searchName)!= 0:
                    try:
                        int(searchName)
                        if len(searchName) ==5:
                            restaurants = target.searchStreetAddressAndZip(searchName,searchName)
                        else:
                            restaurants = target.searchStreetAddressOrName(searchName,00000)
                    except ValueError:
                        
                        restaurants = target.searchStreetAddressOrName(searchName,00000)
                elif len(search) !=0 and len(searchName)== 0:
                    restaurants = target.searchStreetAddressAndZip(search,search)
                elif len(search) !=0 and len(searchName)!= 0:
                    restaurants = target.searchStreetAddressAndZip(search,searchName)

            context.update({'response': "",'restaurants':restaurants,'searchZip':search,'searchName':searchName})
            return render(request,'locations.html',context)

        if len(search)== 5:
            restaurants = target.searchZipCode(search)
            context.update({'response': "",'restaurants':restaurants})
            return render(request,'locations.html',context)
    else:

        target = Restaurant()
        restaurants = target.view_AllRestaurants()
        context.update({'response': "",'restaurants':restaurants})
        return render(request,'locations.html',context)

def searchRestaurant(request):
    if 'auth' in request.session:
        authenticated = request.session['auth']
    else:
        authenticated = False

    if authenticated == True:
        menuIt = MenuItem()
        restaurantID = request.GET['pk']
        menuIt.set_restaurantID(int(restaurantID))
        menuItems = menuIt.viewItems()
        restaurantInfo =  menuIt.viewRestaurant()
        context = get_userinfo(request)
        obj = Account()
        obj.set_accountID(int(request.session['account']))
        address_info = obj.getUserAddress()
        context.update({'menuitems':menuItems,'restaurantInfo':restaurantInfo,'addresses':address_info,'restaurant':restaurantID})
        return render(request,'menu.html',context)
    else:
        menuIt = MenuItem()
        restaurantID = request.GET['pk']
        menuIt.set_restaurantID(int(restaurantID))
        menuItems = menuIt.viewItems()
        restaurantInfo =  menuIt.viewRestaurant()
        context = get_userinfo(request)
        response = "To order you must sign in!"
        context.update({'menuitems':menuItems,'restaurantInfo':restaurantInfo,'restaurant':restaurantID,'response': response, 'alert_flag': True})
        return render(request,'menu.html',context)
