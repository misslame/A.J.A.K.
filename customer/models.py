from django.db import models
from django.db import connection

######### DO NOT CHANGE THE CON. WINDOWS ONLY ALLOWS _CON OR A DIFFERENT NAME COMPLETELY ############
from bearbites._con import getConnection
from bearbites._con import dictfetchall


class Customer(models.Model):
    accountID = []
    customerID = []
    preference= models.CharField(max_length=150)
    preferenceID = models.IntegerField()
    allergyID = models.IntegerField()
    allergy = models.CharField(max_length=128)

    def __str__(self):
        return self.allergy

    def get_acountID(self):
        return self.accountID[0]


    def get_customerID(self):
        return self.customerID[0]


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
        
        

    def addPreference(self):
        try:
            cnxn = getConnection()
            cursor = cnxn.cursor()
            sqlCommand = 'EXEC AddPreference @Customer= {}, @Preference= "{}";'.format(int(self.customerID[0]),self.preference)
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
            cursor.execute('EXEC AddAllergy @Customer= {}, @Allergy= "{}";'.format(int(self.customerID[0]),self.allergy))
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
                sqlCommand = 'EXEC RemovePreference @Customer= {}, @Preference= "{}";'.format(int(self.customerID[0]),self.preference)
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
            cursor.execute('EXEC RemoveAllergy @Customer= {}, @Allergy= "{}";'.format(int(self.customerID[0]),self.allergy))
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
        cursor.execute('EXEC ViewPreferences @User= {};'.format(int(self.customerID[0])))
        rows = cursor.fetchall()
        list_preferences = []
        for row in rows:
            list_preferences.append(str(row[0]))
        return list_preferences

    def viewAllergy(self):
        cnxn = getConnection()
        cursor = cnxn.cursor()
        cursor.execute('EXEC ViewAllergy @User= {};'.format(int(self.customerID[0])))
        rows = cursor.fetchall()
        list_allergy = []
        for row in rows:
            list_allergy.append(str(row[0]))
        return list_allergy