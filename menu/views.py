from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from restaurant.models import Restaurant
from bearbites.models import Account
from .models import Menu, MenuItem
# Create your views here.

