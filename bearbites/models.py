from django.db import models
from django.db import connection
from bearbites._con import getConnection
from bearbites._con import dictfetchall


class Account(models.Model):
    email = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    def __str__(self):
        return self.email

    def get_email(self):
        return self.email
    def set_email( self, mail):
        self.email = mail
    def get_password(self):
        return self.password
    def set_password(self, code):
        self.password = code
    
    def view_users(self):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute("EXEC AllAccounts;")
        cursor.close() #close current connection to db
        cnxn.close()
        del cnxn
        return dictfetchall(cursor) #return query result into dict 


    def getUserAccount(self,email, code):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute('EXEC AccountLookup @UserName={} , @PassCode="{}";'.format(email,code))
        cursor.close() #close current connection to db
        cnxn.close()
        del cnxn
        return dictfetchall(cursor)

    def updateUserAccount(self, account,firstname,lastname, phone, mobile):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute('EXEC UpdateAccount @Account={}, @FirstName="{}" , @LastName="{}", @Phone={}, @MobilePhone={};'.format(account,firstname,lastname, phone, mobile))
        cnxn.commit() #need commit when you are inserting/updating values to a table
        cursor.close() #close current connection to db
        cnxn.close()
        del cnxn
        response = "Account was Updated"
        return response

    def updateUserAddress(self,user,old, description, street, apt,city,state,zipcode):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute('EXEC UpdateAddress @User= {} , @old= "{}" ,@Description= "{}", @StreetAddress= "{}", @AptNum= "{}", @City= "{}", @State= "{}", @Zip= "{}" ;'.format(user,old,description, street, apt,city,state,zipcode))
        cnxn.commit()
        cursor.close()
        cnxn.close()
        del cnxn
        response = "Address was Updated"
        return response
