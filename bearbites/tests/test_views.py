from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest
#from http.cookies import SimpleCookie
from django.urls import reverse
from bearbites.models import Account 
from order.models import Delivery, CartItem, OrderHistory
from customer.models import Customer
from review.models import Review
from menu.models import Menu, MenuItem
from order.views import CreateOrder
from customer.views import loadAllergies, loadPreferences, get_userinfo,lastOrder,loadOrderHistory, loadProfile
from review.views import addReview
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.trial_url = reverse('trial_dashboard1')
        #self.trial2_url = reverse('trial_dashboard2')
        self.register_url = reverse('register_url')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.preference_url = reverse('addPreference_url')
        self.allergy_url = reverse('addAllergy_url')
        self.profile_url = reverse('profile')
        self.edit_profile_url = reverse('profile1')
        self.edit_address_url = reverse('profile2')
        self.address_url = reverse('profile3')
        self.add_review_url = reverse('profile4')
        self.review_history_url = reverse('profile5')
        self.browse_locations_url = reverse('locations')
        self.search_restaurant_url = reverse('searchRestaurant')
        self.create_order_url = reverse('order')

    def test_index_view(self):
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_trialdashboard_view(self):
        response = self.client.get(self.trial_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_register_view(self):
        response = self.client.get(self.register_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_login_view(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout_view(self):
        response = self.client.get(self.logout_url)

        self.assertEquals(response.status_code, 200)

    def test_preference_loggedin_view(self):
        self.client.post('/login/', {'email':'iamironman@si.com', 'password':'W4rm4ch1ne_R0x'})
        response = self.client.get(self.preference_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_preference_loggedout_view(self):
        response = self.client.get(self.preference_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_restrictions_loggedin_view(self):
        self.client.post('/login/', {'email':'iamironman@si.com', 'password':'W4rm4ch1ne_R0x'})
        response = self.client.get(self.allergy_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_restrictions_loggedout_view(self):
        response = self.client.get(self.allergy_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')


    def test_profile_loggedin_view(self):
        self.client.post('/login/', {'email':'iamironman@si.com', 'password':'W4rm4ch1ne_R0x'})
        response = self.client.get(self.profile_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_loggedout_view(self):
        response = self.client.get(self.profile_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_edit_profile_loggedin_view(self):
        self.client.post('/login/', {'email':'iamironman@si.com', 'password':'W4rm4ch1ne_R0x'})
        response = self.client.get(self.edit_profile_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_edit_profile_loggedout_view(self):
        response = self.client.get(self.edit_profile_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_edit_address_loggedin_view(self):
        self.client.post('/login/', {'email':'iamironman@si.com', 'password':'W4rm4ch1ne_R0x'})
        response = self.client.get(self.edit_address_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_edit_address_loggedout_view(self):
        response = self.client.get(self.edit_address_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_address_loggedin_view(self):
        self.client.post('/login/', {'email':'iamironman@si.com', 'password':'W4rm4ch1ne_R0x'})
        response = self.client.get(self.address_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_address_loggedout_view(self):
        response = self.client.get(self.address_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_add_review_submit_view(self):
        self.client.post('/login/', {'email':'iamironman@si.com', 'password':'W4rm4ch1ne_R0x'})
        self.client.post(self.add_review_url, {'reviewID':7, 'reviewType':'Restaurant', 'reviewRating':4, 'reviewComment':'good', 'restaurantRating':4, 'restaurantComment':'good', 'deliveryRating':3, 'deliveryComment':'meh'})
        #self.client.post(self.add_review_url, data={'restaurantRating':4, 'restaurantComment':'good', 'deliveryRating':3, 'deliveryComment':'meh'})
        #self.client.post(self.add_review_url, {'reviewID':7, 'reviewType':'Restaurant', 'reviewRating':4, 'reviewComment':'good', 'deliveryID':17, 'restaurant':2, 'deliveryAddressID':1, 'deliveryDate':'05/15/2020','deliveryTime':'21:32:17', 'deliveryInstructions':'', 'tip':'', 'status':'complete'})
        #response = self.client.get(self.add_review_url)
        #self.factory = RequestFactory()
        #request = self.factory.post('/profile/review/', data, content_type = 'POST')
        response = self.client.get(self.add_review_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_add_review_no_submit_view(self):
        response = self.client.get(self.add_review_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'review.html')

    def test_review_history_loggedin_view(self):
        self.client.post('/login/', {'email':'iamironman@si.com', 'password':'W4rm4ch1ne_R0x'})
        response = self.client.get(self.review_history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_review_history_loggedout_view(self):
        response = self.client.get(self.review_history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_browse_locations(self):
        response = self.client.get(self.browse_locations_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'locations.html')

    def test_search_restaurant_loggedin_view(self):
        self.client.post('/login/', {'email':'iamironman@si.com', 'password':'W4rm4ch1ne_R0x'})
        response = self.client.get(self.search_restaurant_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')

    def test_search_restaurant_loggedout_view(self):
        response = self.client.get(self.search_restaurant_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')

    def test_create_order_loggedin(self):
        self.client.post('/login/', {'email':'iamironman@si.com', 'password':'W4rm4ch1ne_R0x'})
        response = self.client.get(self.create_order_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')

    def test_create_order_loggedout(self):
        response = self.client.get(self.create_order_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')