from django.db import models

# Create your models here.
from django.db import models
from django.db import connection
from bearbites.con import getConnection
from bearbites.con import dictfetchall


class Customer(models.Model):
    customerID = models.IntegerField()
    preferenceName = models.CharField(max_length=150)
    preferenceDescription = models.CharField(max_length=150)
    allergyID = models.IntegerField()
    allergyDescription = models.CharField(max_length=150)

    def __str__(self):
        return self.customerID

    def get_customerID(self):
        return self.customerID

    def set_customerID(self, c_id):
        self.customerID = c_id

    def get_preferenceName(self):
        return self.preferenceName

    def set_preferenceName(self, preference):
        self.preferenceName = preference

    def get_preferenceDescription(self):
        return self.preferenceDescription

    def set_preferenceDescription(self, p_description):
        self.preferenceDescription = p_description

    def get_allergyDescription(self):
        return self.allergyDescription

    def set_allergyDescription(self, a_description):
        self.allergyDescription = a_description

    def get_allergyID(self):
        return self.customerID

    def set_allergyID(self, a_id):
        self.allergyID = a_id


    def addCustomer(self, user):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute("INSERT INTO Customer (UserID) VALUES  ({});".format(user))
        cnxn.commit()
        cursor.close()
        cnxn.close()
        del cnxn
        

    def addPreference(self,customer, name, description):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        sqlCommand = 'EXEC AddPreference @Customer= {}, @Name= "{}", @Description= "{}";'.format(customer,name,description)
        cursor.execute(sqlCommand)
        cnxn.commit()
        cursor.close()
        cnxn.close()
        del cnxn
        response = "Preference was added to account!"
        return response

    def addAllergy(self,customer, allergy, description):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute('EXEC AddAllergy @Customer= {}, @Allergy= {}, @Description= {};'.format(int(customer),int(allergy),description))
        cnxn.commit()
        cursor.close()
        cnxn.close()
        del cnxn
        response = "Allergy added to account"
        return response