from django.test import TestCase
from bearbites.models import Account

class SimpleTest(TestCase):
    # Create your tests here.

    def setUp(self):
        Account.objects.create(email="abynes@yahoo.com")
        

    def test_login(self):
        # Issue a GET request.
       user1 = Account.objects.get(email="abynes@yahoo.com")

       self.assertEqual(user1.checkEmailExists(), True)