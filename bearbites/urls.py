from django.urls import path, include
from django.contrib  import admin
from . import views
from customer import views as account_views
from restaurant import views as restaurant_views



urlpatterns = [
    path('', views.indexView,name = "home"),
    path('dashboard/',views.dashboardView,name="dashboard"),
    path('login/',views.loginView,name="login"),
    path('register/',views.registerView,name="register_url"),
    path('profile/DietaryPreferences/',account_views.customerPreference,name="addPreference_url"),
    path('profile/DietaryRestrictions/',account_views.customerAllergy,name="addAllergy_url"),
    path('profile/',account_views.loadProfile,name="profile"),
    path('profile/EditProfile/',account_views.editProfile,name="edit profile"),
    path('profile/EditAddresses/',account_views.editAddress,name="edit address"),
    path('profile/Addresses/',account_views.loadProfile,name="Addresses"),
    path('locations/', restaurant_views.browseLocationView,name="locations"),
]
