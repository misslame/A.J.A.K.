from django.db import models
from django.db import connection
from bearbites._con import getConnection
from bearbites._con import dictfetchall
# Create your models here.

class Delivery(models.Model):
    deliveryID = models.IntegerField()
    restaurantID = []
    deliveryAddressID = []
    deliveryDate = models.CharField(max_length=128)
    deliveryTime = models.CharField(max_length=128)
    deliveryInstructions = models.CharField(max_length=128)
    tip = models.CharField(max_length=128)
    status = models.CharField(max_length=128)

# Getter Methods
    def __str__(self):
        return self.status

    def get_deliveryID(self):
        return self.delvieryID

    def get_deliveryDate(self):
        return self.deliveryDate

    def get_deliveryTime(self):
        return self.deliveryTime

    def get_deliveryInstructions(self):
        return self.deliveryInstructions

    def get_tip(self):
        return self.tip

    def get_status(self):
        return self.status

#Setter Methods
    def set_deliveryID(self,num):
        self.deliveryID = num

    def set_deliveryDate(self,date):
        self.deliveryDate = date

    def set_deliveryTime(self,time):
        self.deliveryTime = time

    def set_deliveryInstructions(self,instruction):
        self.deliveryInstructions = instruction

    def set_tip(self,money):
        self.tip = money

    def set_status (self,progress):
        self.status = progress

## Database Queries

class CartItem(models.Model):
    cartItemID = models.IntegerField()
    customerID = []
    itemID = []
    specialInstructions = models.CharField(max_length=128)
    quantity = models.IntegerField()

class OrderHistory(models.Model):
    customerID = []
    deliveryID = []
    cartItemID = []
    restaurantID = []
    totalPrice = models.CharField(max_length=128)
