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

# Delivery Propogation
    def processDelivery(self):
        try:
            cnxn = getConnection()
            cursor = cnxn.cursor()
            sql = "EXEC AddDelivery @RestaurantID={}, @AddressID={}, @Date={}, @Time={}, @Instructions={}, @Status={}"
            cursor.execute(sql.format(int(self.restaurantID[0]),int(self.addressID[0]),self.deliveryDate,self.deliveryTime, self.deliveryInstructions,"Order Placed"))
            cnxn.commit()
            cursor.close()
            cnxn.close()
            del cnxn
            response = "Sucesfully Processed Delivery Request"
        except:
            response = "Error Processing Delivery Request"
        return response

# We don't need a delete method, as cancelled orders will be shown in history as "Cancelled"

# Add Tip
    def addTip(self):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        sql = "UPDATE Delivery SET Tip = {} WHERE DeliveryID ={};" # FIX: Needs to be cleaned up to a stored procedure
        cursor.execute(sql.format(self.tip,self.deliveryID))
        cnxn.commit()
        cursor.close()
        cnxn.close()
        del cnxn
        response = "Sucesfully added a tip of ${}".format(self.tip)
        return response

# Check Order Status
    def checkStatus(self):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        sql = "SELECT DeliveryStatus FROM Delivery WHERE DeliveryID={};".format(self.deliveryID)
        cursor.execute(sql)
        return dictfetchall(cursor)

# Update Order Status
    def updateStatus(self):
        try:
            cnxn = getConnection()
            cursor = cnxn.cursor()
            sql = "UPDATE Delivery SET DeliveryStatus = {} WHERE DeliveryID = {};"
            cursor.execute(sql.format(self.status,self.deliveryID))
            cnxn.commit()
            cursor.close()
            cnxn.close()
            del cnxn
            response = "Succesfully Updated Delivery Status"
        except:
            response = "Failed to Update Delivery Status"
        return response

class CartItem(models.Model):
    cartItemID = models.IntegerField()
    customerID = []
    itemID = []
    specialInstructions = models.CharField(max_length=128)
    quantity = models.IntegerField()

# Getter Methods
    def __str__(self):
        return self.cartItemID

    def get_cartItemID(self):
        return self.itemID

    def get_specialInstructions(self):
        return self.specialInstructions

    def get_quantity(self):
        return self.quantity

# Setter Methods
    def set_cartItemID(self,num):
        self.cartItemID = num

    def set_specialInstructions(self,instruction):
        self.specialInstructions = instruction

    def set_quantity(self,amount):
        self.quantity = amount

## Database Queries

# Cart Item Addition
    def addToCart(self):
        try:
            cnxn = getConnection()
            cursor = cnxn.cursor()
            sql = "EXEC AddCartItem @CustomerID={}, @ItemID={}, @SpecialInstructions={}, @Quantity={};"
            formatted = sql.format(int(self.customerID[0]),int(self.itemID[0]),self.specialInstructions,self.quantity)
            cursor.execute(formatted)
            cnxn.commit()
            cursor.close()
            cnxn.close()
            del cnxn
            response = "Sucesfully Added Item to Cart"
        except:
            response = "Error Adding Item to Cart"
        return response

# Cart Item Removal
    def removeFromCart(self):
        try:
            cnxn = getConnection()
            cursor = cnxn.cursor()
            sql = "EXEC RemoveCartItem @CartItemID={}, @CustomerID ={};"
            cursor.execute(sql.format(self.cartItemID,int(self.customerID[0])))
            cnxn.commit()
            cursor.close()
            cnxn.close()
            del cnxn
            response = "Item Succesfully Removed from Cart"
        except:
            response = "Error Removing Item from Cart"
        return response

class OrderHistory(models.Model):
    customerID = []
    deliveryID = []
    cartItemID = []
    restaurantID = []
    totalPrice = models.CharField(max_length=128)

    def get_totalPrice(self):
        return self.totalPrice

    def set_totalPrice(self,total):
        self.totalPrice = total
