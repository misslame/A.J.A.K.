from django.db import models
from django.db import connection
from bearbites._con import getConnection
from bearbites._con import dictfetchall
# Create your models here.

class Restaurant(models.Model):
    accountID = []
    restaurantID = models.IntegerField()
    restaurantName = models.CharField(max_length=128)
    addressID  = []
    orderMin = models.CharField(max_length=128)
    imageURL = models.CharField(max_length=128)
    logoURL = models.CharField(max_length=128)
    zipQuery = []
    nameQuery = []


# Getter Methods
    def __str__(self):
        return self.restaurantName

    def get_accountID(self):
        return self.accountID[0]

    def get_restaurantID(self):
        return self.restaurantID

    def get_restaurantName(self):
        return self.restaurantName

    def get_addressID(self):
        return self.addressID[0]

    def get_orderMin(self):
        return self.get_orderMin

    def get_imageURL(self):
        return self.imageURL

    def get_logoURL(self):
        return self.logoURL

# Setter Methods
    def set_restaurantID(self,restaurant):
        restaurantID = restaurantID

    def set_restaurantName(self,name):
        restaurantName = name

    def set_orderMin(self,min):
        orderMin = min

    def set_imageURL(self,url):
        imageURL = url

    def set_logoURL(self,url):
        logoURL = url

## Database Queries

# Restaurant Propogation
    def addRestaurant(self):
        try:
            cnxn = getConnection()
            cursor = cnxn.cursor() # Establish Connection to the Database
            sql = "EXEC AddRestaurant @UserID={}, @RestaurantName={}, @AddressID ={}, @OrderMin={}, @ImageUrl={}, @LogoUrl={};" # SQL Stored Procedure
            cursor.execute(sql.format(int(self.accountID[0]),self.restaurantName,int(self.addressID[0]),self.orderMin,self.imageURL,self.logoURL)) # Fill Command with Data and Execute
            cnxn.commit()
            cursor.close()
            cnxn.close()
            del cnxn
            response = "Restaurant Succesfully Created"
        except:
            response = "Error Creating Restaurant"
        return response

# Restaurant Deletion
    def deleteRestaurant(self):
        try:
            cnxn = getConnection()
            cursor = cnxn.cursor() # Establish Connection to the Database
            sql = "EXEC RemoveRestuarant @UserID={}, @Restaurant={}" # SQL Stored Procedure
            cursor.execute(sql.format(int(self.accountID[0]),int(self.addressID[0]))) #Delete Based on AccountID and addressID
            cnxn.commit()
            cursor.close()
            cnxn.close()
            del cnxn
            response = "Restuarant succefully deleted"
        except:
            response = "Error deleting Restaurant"
        return response

# Restaurant Querying

# Single Query (For Popout)
    def viewRestaurant(self):
        cnxn = getConnection()
        cursor = cnxn.cursor() # Establish Conenction to the Database
        sql = "SELECT * FROM Restaurant WHERE RestaurantID = {};".format(int(restaurantID)) # FIX: Needs to be cleaned up to a stored procedure
        cursor.execute(sql)
        row = cursor.fetchall() # Store Values from Query
        print(row) #Assuming row is a 1-D Array of Table Columns
        row_entries = []
        for col in row: #Cast row values to strings
            row_entries.append(str(col))
        cursor.close()
        cnxn.close()
        del cnxn
        return row_entries

# Zip Code Query
    def searchZipCode(self):
        cnxn = getConnection()
        cursor = cnxn.cursor() #Establish Connection to the Database
        sql = "SELECT AddressID FROM Adresses WHERE Zip = {} INTERSECT SELECT AddressID FROM Restaurant;" #Returns All Adress IDs in Given Zip Code
        cursor.execute(sql.format(int(zipQuery[0])))
        adresses = cursor.fetchall()
        restaurants = []
        sql_restaurant = "SELECT * FROM Restaurant WHERE AddressID IN {};" # FIX: Needs to be cleaned up to a stored procedure
        cursor2 = cnxn.cursor()
        cursor2.execute(sql.format(tuple(addresses)))
        rows = cursor2.fetchall()
        for row in rows:
            restaurants.append(str(rows[0]))
        cursor.close()
        cursor2.close()
        cnxn.close()
        del cnxn
        return restaurants
