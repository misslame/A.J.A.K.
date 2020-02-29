from django.db import models
from django.db import connection
from bearbites.con import getConnection
from bearbites.con import dictfetchall


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
        row = cursor.execute("EXEC AllAccounts;")
        return dictfetchall(cursor)
    def getUserAccount(self, mail, code):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute("EXEC AccountLookup @UserName=admin , @PassCode=testbear;")
        return dictfetchall(cursor)



# Create your models here.
