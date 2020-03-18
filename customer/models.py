from django.db import models
from django.db import connection
from bearbites._con import getConnection
from bearbites._con import dictfetchall


class Customer(models.Model):
    accountID = models.IntegerField()
    customerID = models.IntegerField()
    preference= models.CharField(max_length=150)
    preferenceID = models.IntegerField()
    allergyID = models.IntegerField()
    allergy = models.CharField(max_length=128)

    def __str__(self):
        return self.customerID

    def get_acountID(self):
        return self.accountID

    def set_accountID(self, a_id):
        self.accountID = a_id

    def get_customerID(self):
        return self.customerID

    def set_customerID(self, c_id):
        self.customerID = c_id

    def get_preference(self):
        return self.preference

    def set_preference(self, pref):
        self.preference = pref

    def get_preferenceID(self):
        return self.preferenceID

    def set_preferenceID(self, p_id):
        self.preferenceID = p_id

    def get_allergy(self):
        return self.allergy

    def set_allergy(self, allerg):
        self.allergy = allerg

    def get_allergyID(self):
        return self.allergyID

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
        
        

    def addPreference(self):
        try:
            cnxn = getConnection()
            cursor = cnxn.cursor()
            sqlCommand = 'EXEC AddPreference @Customer= {}, @Preference= "{}";'.format(self.customerID,self.preference)
            cursor.execute(sqlCommand)
            cnxn.commit()
            cursor.close()
            cnxn.close()
            del cnxn
            response = "Preference was added to account!"
        except:
            response = "An Error Occured Adding The Preference To The Account"
        return response

    def addAllergy(self):
        try:
            cnxn = getConnection()
            cursor = cnxn.cursor()
            cursor.execute('EXEC AddAllergy @Customer= {}, @Allergy= "{}";'.format(self.customerID,self.allergy))
            cnxn.commit()
            cursor.close()
            cnxn.close()
            del cnxn
            response = "Allergy added to account"
        except:
            response = "An Error Occured Adding The Allergy To The Account"
        return response

    def removePreference(self):
            try:
                cnxn = getConnection()
                cursor = cnxn.cursor()
                sqlCommand = 'EXEC RemovePreference @Customer= {}, @Preference= "{}";'.format(self.customerID,self.preference)
                cursor.execute(sqlCommand)
                cnxn.commit()
                cursor.close()
                cnxn.close()
                del cnxn
                response = "Preference was removed from  account!"
            except:
                response = "An Error Occured Removing The Preference To The Account"
            return response

    def removeAllergy(self):
        try:
            cnxn = getConnection()
            cursor = cnxn.cursor()
            cursor.execute('EXEC RemoveAllergy @Customer= {}, @Allergy= "{}";'.format(self.customerID,self.allergy))
            cnxn.commit()
            cursor.close()
            cnxn.close()
            del cnxn
            response = "Allergy removed from account"
        except:
            response = "An Error Occured Removing The Allergy To The Account"
        return response

    def viewPreferences(self):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute('EXEC ViewPreferences @User= {};'.format(self.customerID))
        rows = cursor.fetchall()
        list_preferences = []
        for row in rows:
            list_preferences.append(str(row[0]))
        return list_preferences

    def viewAllergy(self):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute('EXEC ViewAllergy @User= {};'.format(self.customerID))
        rows = cursor.fetchall()
        list_allergy = []
        for row in rows:
            list_allergy.append(str(row[0]))
        return list_allergy