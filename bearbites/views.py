import re
from django.shortcuts import render
from django.http import HttpResponse
from .models import Account
from django.template import Context, loader



def indexView(request):

    
    account =  Account()
    row = account.view_users()
    context = {'users': row}
    return render(request, 'index.html', context)
    

def dashboardView(request):
    return render(request,'index.html')

def registerView(request):
    return render(request,'register.html')