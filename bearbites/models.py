from django.db import models
from django.db import connection

######### DO NOT CHANGE THE CON. WINDOWS ONLY ALLOWS _CON OR A DIFFERENT NAME COMPLETELY ############
from bearbites._con import getConnection
from bearbites._con import dictfetchall




class Account(models.Model):
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    phone = models.IntegerField()
    mobile = models.IntegerField()
    accountID = models.IntegerField()

    
    addrressName= models.CharField(max_length=124)
    aptnum = models.CharField(max_length=24)
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=60)
    zipcode = models.IntegerField()
    userAuthenticated = models.BooleanField()

    def __str__(self):
        return self.email
    
    
    def set_userAuthenticated(self, auth):
        self.userAuthenticated = auth
    
    def get_userAuthenticated(self):
        return self.userAuthenticated

    def get_accountID(self):
        return self.accountID

    def set_accountID( self, usr):
        self.accountID = usr

    def get_firstname(self):
        return self.firstname
        
    def set_firstname( self, first):
        self.firstname = first

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
    
    def set_email( self, eml):
        self.email = eml

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def set_password(self, code):
        self.password = code

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

    def authenticateCustomer(self):      
        cnxn = getConnection()
        cursor2 = cnxn.cursor()
        sqlcommand = "select UserID from UserAccount  where Email='{}' and Password='{}';".format(self.email,self.password)
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
        sqlcommand = "select CONCAT(FirstName, ' ', LastName) from UserAccount  where Email='{}' and Password='{}';".format(self.email,self.password)
        cursor3 = cnxn.cursor()
        cursor3.execute(sqlcommand)  
        rows3 = cursor3.fetchall()
        for row in rows3:
            user.append(str(row[0])) 
        self.userAuthenticated = True   
        cursor.close()
        cursor2.close()
        cursor3.close()
        cnxn.close()
        del cnxn
        return user

    def view_users(self):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute("EXEC AllAccounts;")
        return dictfetchall(cursor) #return query result into dict 

    def getUserAccount(self):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute('EXEC AccountLookup @UserName="{}" , @PassCode="{}";'.format(self.email,self.password))
        return dictfetchall(cursor)

    def getUserAddress(self):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute('EXEC AddressLookup @User={} , @Description="Main";'.format(self.accountID))
        return dictfetchall(cursor)

    def updateUserAccount(self):
        try:
            cnxn = getConnection()
            cursor = cnxn.cursor()
            cursor.execute('EXEC UpdateAccount @Account={}, @FirstName="{}" , @LastName="{}", @Phone={};'.format(self.accountID,self.firstname,self.lastname, self.phone))
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
        sqlcommand = 'EXEC RegisterAccount @FirstName="{}", @LastName="{}", @Phone={}, @Mobile={}, @Email="{}", @Password ="{}";'.format(self.firstname,self.lastname,self.phone,self.mobile,self.email,self.password)
        print (sqlcommand)
        cursor.execute(sqlcommand)
        cnxn.commit()
        cursor2 = cnxn.cursor()
        sqlcommand = "select UserID from UserAccount  where Email='{}' and Password='{}';".format(self.email,self.password)
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
            sqlcommand = 'EXEC RegisterAddress @User= {} , @Name= "{}", @StreetAddress= "{}", @AptNum= "{}", @City= "{}", @State= "{}", @Zip= {} ;'.format(int(self.accountID),self.addrressName, self.street, self.aptnum,self.city,self.state,self.zipcode)
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
            cursor.execute('EXEC UpdateAddress @User= {} , @old= "{}" ,@Description= "{}", @StreetAddress= "{}", @AptNum= "{}", @City= "{}", @State= "{}", @Zip= "{}" ;'.format(self.accountID,old,self.addrressName, self.street, self.aptnum,self.city,self.state,self.zipcode))
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
        cursor.execute('EXEC LookUpUserAddress @User = {};'.format(self.accountID))
        return dictfetchall(cursor) #return query result into dict 

    def get_AddressID(self):
        cnxn = getConnection()     
        cursor=cnxn.cursor()
        sql = "EXEC FindAddress @User = {}, @Street='{}', @Apt ='{}'".format(self.accountID, self.street,self.aptnum)
        print(sql)
        cursor.execute(sql)
        list = cursor.fetchall()
        return list[0][0]
        

# Create your models here.

