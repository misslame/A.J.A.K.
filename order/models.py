from django.db import models
from django.db import connection
from bearbites._con import getConnection
from bearbites._con import dictfetchall
from customer.models import Customer
from menu.models import MenuItem
# Create your models here.

class Delivery(Customer):
    deliveryID = models.IntegerField()
    restaurant = models.IntegerField()
    deliveryAddressID = models.IntegerField()
    deliveryDate = models.CharField(max_length=128)
    deliveryTime = models.CharField(max_length=128)
    deliveryInstructions = models.CharField(max_length=128)
    tip = models.CharField(max_length=128)
    status = models.CharField(max_length=128)

# Getter Methods
    def __str__(self):
        return self.status

    def get_deliveryID(self):
        return self.deliveryID

    def get_restaurant(self):
        return self.restaurant

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

    def set_restaurant(self,res):
        self.restaurant = res

    def set_deliveryAddressID(self,add):
        self.deliveryAddressID = add

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
            sql = "EXEC AddDelivery @RestaurantID={}, @AddressID={}, @Date='{}', @Time='{}', @Instructions='{}', @Status='{}'"
            sql = sql.format(int(self.restaurant),int(self.deliveryAddressID),self.deliveryDate,self.deliveryTime, self.deliveryInstructions,"Order Placed")
            print(sql)
            cursor.execute(sql)
            cnxn.commit()
            cursor.close()
            cursor2 = cnxn.cursor()
            query = "SELECT DeliveryID FROM Delivery WHERE DeliveryAddressID = {};".format(int(self.deliveryAddressID))
            print(query)
            cursor2.execute(query)
            results = cursor2.fetchall()
            response = results[-1][0]
            cursor2.close()
            cnxn.close()
            del cnxn
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

class CartItem(MenuItem):
    cartItemID = models.IntegerField()
    
   
    specialInstructions = models.CharField(max_length=128)
    quantity = models.IntegerField()

# Getter Methods
    def __str__(self):
        return self.cartItemID

    def get_cartItemID(self):
        return self.cartItemID

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
            sql = "EXEC AddCartItem @CustomerID={}, @ItemID={}, @SpecialInstructions='{}', @Quantity={};"
            formatted = sql.format(int(self.customerID),int(self.itemID),self.specialInstructions,int(self.quantity))
            print(formatted)
            cursor.execute(formatted)
            cnxn.commit()
            sql = "select CartItemID FROM CartItems WHERE CustomerID = {} AND ItemID={}".format(int(self.customerID),int(self.itemID))
            cursor.execute(sql)
            response = cursor.fetchall()
            itemValue = response[-1][0]
            cursor.close()
            cnxn.close()
            del cnxn
            return itemValue
        except:
            response = "Error Adding Item to Cart"
        return response

# Cart Item Removal
    def removeFromCart(self):
        try:
            cnxn = getConnection()
            cursor = cnxn.cursor()
            sql = "EXEC RemoveCartItem @CartItemID={}, @CustomerID ={};"
            cursor.execute(sql.format(self.cartItemID,int(self.customerID)))
            cnxn.commit()
            cursor.close()
            cnxn.close()
            del cnxn
            response = "Item Succesfully Removed from Cart"
        except:
            response = "Error Removing Item from Cart"
        return response

class OrderHistory(CartItem,Delivery):
    
    def createOrder(self):
        try:
            cnxn = getConnection()
            cursor = cnxn.cursor()
            sql = "insert into OrderHistory VALUES( {}, {}, {});".format(int(self.customerID),int(self.deliveryID),int(self.cartItemID))
            print(sql)
            cursor.execute(sql)
            cnxn.commit()
            cursor.close()
            cnxn.close()
            del cnxn
            response = "Succesfully Placed Your Order. It's on its way"
        except:
            response = "Error placing order, please try again"
        return response



    