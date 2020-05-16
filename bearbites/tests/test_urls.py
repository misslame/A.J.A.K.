from django.test import SimpleTestCase
from django.urls import reverse, resolve
from bearbites.views import indexView, registerView, loginView, logout #, profileView, orderView, trialDashBoardView
from customer.views import loadAllergies, loadPreferences, get_userinfo,lastOrder,loadOrderHistory, loadProfile, editProfile, editAddress, customerAllergy, customerPreference, loadCustomerReviews 
from order.views import CreateOrder
from order.models import OrderHistory
from review.views import addReview
from restaurant.views import browseLocationView, searchRestaurant

class TestURLs(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEquals(resolve(url).func, indexView)

    def test_dashboard_url_resolves(self):
        url = reverse('trial_dashboard1')
        print(resolve(url))
        self.assertEquals(resolve(url).func, indexView)

    # def test_trial_dashboard_url_resolves(self):
    #     url = reverse('trial_dashboard2')
    #     print(resolve(url))
    #     self.assertEquals(resolve(url).func, trialDashBoardView)

    def test_login_url_resolves(self):
        url = reverse('login')
        print(resolve(url))
        self.assertEquals(resolve(url).func, loginView)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        print(resolve(url))
        self.assertEquals(resolve(url).func, logout)

    def test_register_url_resolves(self):
        url = reverse('register_url')
        print(resolve(url))
        self.assertEquals(resolve(url).func, registerView)

    def test_order_url_resolves(self):
        url = reverse('order')
        print(resolve(url))
        self.assertEquals(resolve(url).func, CreateOrder)

    def test_preference_url_resolves(self):
        url = reverse('addPreference_url')
        print(resolve(url))
        self.assertEquals(resolve(url).func, customerPreference)

    def test_restrictions_url_resolves(self):
        url = reverse('addAllergy_url')
        print(resolve(url))
        self.assertEquals(resolve(url).func, customerAllergy)

    def test_profile_url_resolves(self):
        url = reverse('profile')
        print(resolve(url))
        self.assertEquals(resolve(url).func, loadProfile)

    def test_edit_profile_url_resolves(self):
        url = reverse('profile1')
        print(resolve(url))
        self.assertEquals(resolve(url).func, editProfile)

    def test_edit_address_url_resolves(self):
        url = reverse('profile2')
        print(resolve(url))
        self.assertEquals(resolve(url).func, editAddress)

    def test_addresses_url_resolves(self):
        url = reverse('profile3')
        print(resolve(url))
        self.assertEquals(resolve(url).func, loadProfile)

    def test_add_review_url_resolves(self):
        url = reverse('profile4')
        print(resolve(url))
        self.assertEquals(resolve(url).func, addReview)

    def test_load_review_url_resolves(self):
        url = reverse('profile5')
        print(resolve(url))
        self.assertEquals(resolve(url).func, loadCustomerReviews)

    def test_locations_url_resolves(self):
        url = reverse('locations')
        print(resolve(url))
        self.assertEquals(resolve(url).func, browseLocationView)

    def test_search_url_resolves(self):
        url = reverse('searchRestaurant')
        print(resolve(url))
        self.assertEquals(resolve(url).func, searchRestaurant)