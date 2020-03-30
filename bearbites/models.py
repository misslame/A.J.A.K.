from django.db import models
from django.db import connection

######### DO NOT CHANGE THE CON. WINDOWS ONLY ALLOWS _CON OR A DIFFERENT NAME COMPLETELY ############
from bearbites._con import getConnection
from bearbites._con import dictfetchall

cust_id = 0
acct = 0


class Account(models.Model):
    email = []
    password = []
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    mail = models.CharField(max_length=128)
    passcode = models.CharField(max_length=128)
    phone = models.IntegerField()
    mobile = models.IntegerField()
    account = models.IntegerField()

    addrressName= models.CharField(max_length=124)
    aptnum = models.CharField(max_length=24)
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=60)
    zipcode = models.IntegerField()
    userAuthenticated = []
    accountID = []
    customerID = []


    def __str__(self):
        return self.email
    
    def get_userAuthenticated(self):
        return self.userAuthenticated[0]

    def get_accountID(self):
        return self.accountID[0]

    def get_customerID(self):
        return self.customerID[0]

    def set_accountID( self, usr):
        self.account = usr

    def get_firstname(self):
        return self.firstname
        
    def set_firstname( self, first):
        self.firstname = first
    
        
    def set_email( self, eml):
        self.mail = eml


    def get_lastname(self):
        return self.lastname
        
    def set_lastname( self, last):
        self.lastname = last

    def get_phone(self):
        return self.phone

    def set_phone( self, pho):
        self.phone = pho

    def get_mobile(self):
        return self.mobile

    def set_mobile( self, cell):
        self.mobile = cell

    def get_email(self):
        return self.email[0]


    def get_password(self):
        return self.password[0]

    def set_password(self, code):
        self.passcode = code

    def get_aptnum(self):
        return self.aptnum
        
    def set_aptnum( self, apt):
        self.aptnum = apt

    def get_street(self):
        return self.street
        
    def set_street( self, adrs):
        self.street = adrs

    def get_city(self):
        return self.city
        
    def set_city( self, cty):
        self.city = cty

    def get_state(self):
        return self.state
        
    def set_state( self, ste):
        self.state = ste

    def get_zipcode(self):
        return self.zipcode
        
    def set_zipcode( self, zip):
        self.zipcode = zip

    def get_addressName(self):
        return self.addrressName
        
    def set_addressName( self, adrsn):
        self.addrressName = adrsn

    def authenticateUser(self):      
        cnxn = getConnection()
        cursor2 = cnxn.cursor()
        sqlcommand = "select UserID from UserAccount  where Email='{}' and Password='{}';".format(self.email[0],self.password[0])
        cursor2.execute(sqlcommand)  
        rows = cursor2.fetchall()
        user = []
        for row in rows:
            user.append(str(row[0]))
        cursor = cnxn.cursor()
        sqlcommand = "select CustomerID from Customer  where UserID={} ;".format(int(user[0]))
        cursor.execute(sqlcommand)  
        rows2 = cursor.fetchall()
        for row in rows2:
            print(row)
            user.append(str(row[0]))    
        cursor.close()
        cursor2.close()
        cnxn.close()
        del cnxn
        return user

    def addCustomer(self):
        try:
            cnxn = getConnection() 
            cursor = cnxn.cursor()
            cursor.execute("INSERT INTO Customer (UserID) VALUES  ({});".format(self.account))
            cnxn.commit()
            cursor.close()
            cnxn.close()
            del cnxn
            response = "Account was created, please login"
        except:
            response = "An Error Ocurred While Creating Account, Please Try Again"
        return response



    def view_users(self):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute("EXEC AllAccounts;")
        return dictfetchall(cursor) #return query result into dict 


    def getUserAccount(self):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute('EXEC AccountLookup @UserName="{}" , @PassCode="{}";'.format(self.email[0],self.password[0]))
        return dictfetchall(cursor)

    def getUserAddress(self):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute('EXEC AddressLookup @User={} , @Description="Main";'.format(self.accountID[0]))
        return dictfetchall(cursor)

    def updateUserAccount(self):
        try:
            cnxn = getConnection()
            cursor = cnxn.cursor()
            cursor.execute('EXEC UpdateAccount @Account={}, @FirstName="{}" , @LastName="{}", @Phone={};'.format(self.accountID[0],self.firstname,self.lastname, self.phone))
            cnxn.commit() #need commit when you are inserting/updating values to a table
            cursor.close() #close current connection to db
            cnxn.close()
            del cnxn
            response = "Account was Updated"
        except:
            response = "An Error Ocurred While Updating Account, Please Try Again"
        return response


    def addUserAccount(self):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        sqlcommand = 'EXEC RegisterAccount @FirstName="{}", @LastName="{}", @Phone={}, @Mobile={}, @Email="{}", @Password ="{}";'.format(self.firstname,self.lastname,self.phone,self.mobile,self.mail,self.passcode)
        print (sqlcommand)
        cursor.execute(sqlcommand)
        cnxn.commit()
        cursor2 = cnxn.cursor()
        sqlcommand = "select UserID from UserAccount  where Email='{}' and Password='{}';".format(self.email[0],self.password[0])
        print (sqlcommand)
        cursor2.execute(sqlcommand)  
        rows = cursor2.fetchall()
        user = []
        for row in rows:
            user.append(str(row[0]))
        cursor.close()
        cursor2.close()
        cnxn.close()
        del cnxn
        print(user[0])
        return user[0]

    def addAddress(self):
        try:
            cnxn = getConnection()
            cursor = cnxn.cursor()
            sqlcommand = 'EXEC RegisterAddress @User= {} , @Name= "{}", @StreetAddress= "{}", @AptNum= "{}", @City= "{}", @State= "{}", @Zip= {} ;'.format(int(self.account),self.addrressName, self.street, self.aptnum,self.city,self.state,self.zipcode)
            print(sqlcommand)
            cursor.execute(sqlcommand)
            cnxn.commit()
            cursor.close()
            cnxn.close()
            del cnxn
            response = "Address was Added"
        except:
            response = "An Error Occured Adding The Address"

        return response

    def updateUserAddress(self,old):
        try:
            cnxn = getConnection()
            cursor = cnxn.cursor()
            cursor.execute('EXEC UpdateAddress @User= {} , @old= "{}" ,@Description= "{}", @StreetAddress= "{}", @AptNum= "{}", @City= "{}", @State= "{}", @Zip= "{}" ;'.format(self.accountID[0],old,self.addrressName, self.street, self.aptnum,self.city,self.state,self.zipcode))
            cnxn.commit()
            cursor.close()
            cnxn.close()
            del cnxn
            response = "Address was Updated"
        except:
            response = "An Error Occured Updating The Address"

        return response

    def checkEmailExists(self, email):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute("select UserID  from UserAccount where Email= '{}';".format(email))
        rows = cursor.fetchall()
        if len(rows)==0:
            return False
        else:
            return True #return True if an account exsists with that email 

    def view_userAddresses(self):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute('EXEC LookUpUserAddress @User = "{}";'.format(self.accountID[0]))
        return dictfetchall(cursor) #return query result into dict 



# Create your models here.
