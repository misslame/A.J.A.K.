from django.urls import path, include
from django.contrib  import admin
from . import views


urlpatterns = [
    path('', views.indexView,name = "home"),
    path('dashboard/',views.dashboardView,name="dashboard"),
    path('login/',views.loginView,name="login"),
    path('register/',views.registerView,name="register"),
    path('profile/',views.profileView,name="profile"),
]