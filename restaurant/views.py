from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from .models import Restaurant
from bearbites.models import Account
# Create your views here.

def browseLocationView(request):

    if request.method == 'POST':
        target = Restaurant()
        target.zipQuery.clear()
        zip = request.POST.get('search')
        isInteger = False
        try:
            float(zip)
        except ValueError:
            response = "Not a Valid 5-Digit Zip Code. Try Again!"
            context = {'response': response}
            return render(request,'locations.html',context)
        else:
            isInteger=float(zip).is_integer()
        if isInteger == True:
            zip = int(zip)
            target.zipQuery.append(zip)
            context = target.searchZipCode()
        return render(request,'locations.html',context)
    else:
        target = Restaurant()
        restaurants = target.view_AllRestaurants()
        context = {'response': "",'restaurants':restaurants}
        
        return render(request,'locations.html',context)
