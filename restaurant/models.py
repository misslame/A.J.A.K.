from django.db import models
from django.db import connection
from bearbites._con import getConnection
from bearbites._con import dictfetchall

# Create your models here.

class Restaurant():

    restaurantID = models.IntegerField()
    restaurantName = models.CharField(max_length=128)
    orderMin = models.CharField(max_length=128)
    imageURL = models.CharField(max_length=128)
    logoURL = models.CharField(max_length=128)
    zipQuery = []
    nameQuery = []


# Getter Methods
    def __str__(self):
        return self.restaurantName

    def get_restaurantID(self):
        return self.restaurantID

    def get_restaurantName(self):
        return self.restaurantName


    def get_orderMin(self):
        return self.get_orderMin

    def get_imageURL(self):
        return self.imageURL

    def get_logoURL(self):
        return self.logoURL

# Setter Methods
    def set_restaurantID(self,restaurant):
        self.restaurantID = restaurant

    def set_restaurantName(self,name):
        self.restaurantName = name

    def set_orderMin(self,min):
        self.orderMin = min

    def set_imageURL(self,url):
        self.imageURL = url

    def set_logoURL(self,url):
        self.logoURL = url



## Database Queries

# Restaurant Propogation
    def addRestaurant(self):
        try:
            cnxn = getConnection()
            cursor = cnxn.cursor() # Establish Connection to the Database
            sql = 'EXEC AddRestaurant @UserID={}, @RestaurantName="{}", @AddressID ={}, @OrderMin={}, @ImageUrl="{}", @LogoUrl="{}";' # SQL Stored Procedure
            cursor.execute(sql.format(int(self.accountID),self.restaurantName,int(self.addressID[0]),self.orderMin,self.imageURL,self.logoURL)) # Fill Command with Data and Execute
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
            sql = "EXEC RemoveRestuarant @UserID={}, @Restaurant={};" # SQL Stored Procedure
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
        cursor = cnxn.cursor()
        cursor.execute('EXEC ViewRestaurantDetails @Restaurant = {};'.format(int(self.restaurantID)))
        return dictfetchall(cursor) #return query result into dict

    # Restaurant Name Query
    def searchName(self):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute('EXEC ViewRestaurantByName @Name = "%{}%";'.format(self.restaurantName))
        return dictfetchall(cursor) #return query result into dict

# Zip Code Query
    def searchZipCode(self,zip):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute('EXEC ViewRestaurantByZip @Zip = {},  @Street="%{}%";'.format(int(zip),zip))
        print('EXEC ViewRestaurantByZip @Zip = {},  @Street="%{}%";'.format(int(zip),zip))
        return dictfetchall(cursor) #return query result into dict

# Street Address Query
    def searchStreetAddress(self,street):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute('EXEC ViewRestaurantByStreet @Street ="%{}%";'.format(street))
        return dictfetchall(cursor) #return query result into dict

# Street Address or Restaurant Name Query
    def searchStreetAddressOrName(self,value,zip):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        sqlcommand = 'EXEC ViewRestaurantByStreetOrNameOrZip @Value ="%{}%" , @Zip={};'.format(value,zip)
        print(sqlcommand)
        cursor.execute(sqlcommand)
        return dictfetchall(cursor) #return query result into dict

# Street Address and Restaurant Name Query
    def searchStreetAddressAndZip(self,zip,value):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        
        if zip in value:
            sqlcommand = 'EXEC ViewRestaurantByStreetOrName @Zip={}, @Value ="%{}%";'.format(int(zip),value)
        else:
            sqlcommand = 'EXEC ViewRestaurantByStreetOrName @Zip={}, @Value ="%{}%";'.format(int(zip),value)
        print(sqlcommand)
        cursor.execute(sqlcommand)
        return dictfetchall(cursor) #return query result into dict

# Finding a Specific Restaurant Location
    def fetchLocation(self,location):
        cnxn = getConnection()
        cursor= cnxn.cursor() #Establish Connection to the Database
        sql = "SELECT AddressID FROM Adresses WHERE StreetAddress = {};" #Find all Addresses at that location
        cursor.execute(sql.format(location))
        potential = cursor.fetchall()
        sql2 = "SELECT RestaurantID FROM Restaurant WHERE AddressID IN {} AND RestuarantName = {};" #FIX: Clean up to stored procedure
        cursor2 = cnxn.cursor() #Filter Adresses to the Restaurant ID Matching that Specific Restaurant
        cursor2.execute(sql2.format(str(tuple(potential)),self.restaurantName))
        idNum = cursor2.fetchall()
        return idNum[0]

    def view_AllRestaurants(self):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute('EXEC ViewRestaurants;')
        return dictfetchall(cursor) #return query result into dict

    def view_RestaurantReviews(self):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute('EXEC viewRestaurantReviews  @Restaurant={}'.format(int(self.restaurantID)))
        return dictfetchall(cursor) #return query result into dict
