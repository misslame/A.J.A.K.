import re
from django.shortcuts import render
from django.http import HttpResponse
from .models import Account
from django.template import Context, loader



def indexView(request):

    return render(request, 'index.html')
    

def dashboardView(request):
    return render(request,'index.html')

def registerView(request):
    if request.method == 'POST': # If the form has been submitted...
        
        obj = Account()
        obj.set_firstname(request.POST.get('firstname'))
        obj.set_lastname(request.POST.get('lastname'))
        obj.set_mobile(int(request.POST.get('phonenumber')))
        obj.set_phone(int(request.POST.get('phonenumber')))
        obj.set_email(request.POST.get('email'))
        obj.set_password(request.POST.get('password'))
        obj.set_addressName("Main")
        obj.set_aptnum(request.POST.get('aptNum'))
        obj.set_street(request.POST.get('street'))
        obj.set_city(request.POST.get('city'))
        obj.set_state(request.POST.get('state'))
        obj.set_zipcode(int(request.POST.get('zip')))
        user = int(obj.addUserAccount())
        print (user)
        obj.set_user(int(user))
        obj.addAddress()
        response = "Account Added"
        context = {'response': response}
        return render(request,'register.html', context)
    else :
        return render(request,'register.html')

def loginView(request):
    return render(request,'login.html')

def profileView(request):
    return render(request,'profile.html')