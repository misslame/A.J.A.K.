from django.urls import path, include
from django.contrib  import admin
from . import views
from customer import views as account_views
from restaurant import views as restaurant_views
from menu import views as menu_views
from order import views as order_views
from review import views as review_views

urlpatterns = [
    path('', views.indexView,name = "home"),
    path('dashboard/',views.indexView,name="trial_dashboard1"),
    path('login/',views.loginView,name="login"),
    path('logout/',views.logout,name="logout"),
    path('register/',views.registerView,name="register_url"),
    #path('trial_dashboard/',views.trialDashBoardView,name="trial_dashboard2"),


    # Customer Profile Page:
    path('profile/DietaryPreferences/',account_views.customerPreference,name="addPreference_url"),
    path('profile/DietaryRestrictions/',account_views.customerAllergy,name="addAllergy_url"),
    path('profile/',account_views.loadProfile,name="profile"),
    path('profile/EditProfile/',account_views.editProfile,name="profile1"),
    path('profile/EditAddresses/',account_views.editAddress,name="profile2"),
    path('profile/Addresses/',account_views.loadProfile,name="profile3"),
    path('profile/review/',review_views.addReview, name="profile4"),
    path('profile/ReviewHistory/',account_views.loadCustomerReviews, name="profile5"),
    
    # Browse locations Page
    path('locations/', restaurant_views.browseLocationView,name="locations"),

    path('searchRestaurant/', restaurant_views.searchRestaurant,name="searchRestaurant"),

    path('order/',order_views.CreateOrder,name="order"),


]
