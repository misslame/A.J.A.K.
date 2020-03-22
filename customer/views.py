from django.shortcuts import render
from .models import Customer
from bearbites.models import Account
# Create your views here.
checkbox_list = ['Milk', 'Eggs', 'True Nuts', 'Wheat', 'Peanuts', 'Soy','Fish','ShellFish']
p_checkbox_list = ['Diabetic', 'Gluten-Free', 'Vegetarian', 'Vegan', 'Pescatarian', 'Kosher','Paleo Diet','Mediterranean Diet', 'Keto Diet', 'High Protein', 'Low Carb', 'Low Fat', 'Raw Food', 'Fast Food','Street Food','Fresh Food', 'Seafood','Sugar-Free','Low-Sodium','Low-Cholesterol','Organic', 'Non-GMO','Asian','African','American','Latin','European','Middle Eastern','Pasific']
def loadAllergies():
    obj = Customer()
    obj2 = Account()
    print (obj2.get_customerID())
    allergy_list = obj.viewAllergy()
    num_allergies = len(allergy_list)
    list_check = []
    total_allergies = 0
    if num_allergies > 0:    
        for check in checkbox_list:
            if total_allergies <= num_allergies:
                found = 0
                for allergy in allergy_list:
                    if check in allergy:
                        found = 1
                        break
                if found == 1:
                    list_check.append("checked")
                    total_allergies += 1
                else:
                    list_check.append("")
            else:
                list_check.append("")
    else:
        list_check = [""] * len(checkbox_list)
    return list_check

def loadPreferences():
    obj = Customer()
    obj2 = Account()
    preferences_list = obj.viewPreferences()
    num_preferences = len(preferences_list)
    list_check = []
    total_preferences = 0
    if num_preferences > 0:
        for check in p_checkbox_list:
            if total_preferences <= num_preferences:
                found = 0
                for preference in preferences_list:
                    if check in preference:
                        found = 1
                        break
                if found == 1:
                    list_check.append("checked")
                    total_preferences += 1
                else:
                    list_check.append("")
            else:
                list_check.append("")
    else:
        list_check = [""] * len(p_checkbox_list)
    return list_check

def loadProfile(request):
    obj = Account()
    authenticated = obj.get_userAuthenticated()
    if authenticated in "TRUE":
        allergies = loadAllergies()
        preferences = loadPreferences()
        user_info = obj.getUserAccount()
        address_info = obj.getUserAddress()
        print(user_info)
        print(obj.get_accountID())

        return render(request, 'profile.html', {'check_list': allergies,'p_check_list': preferences ,'users': user_info,'addresses': address_info })
    else:
        return render(request,'login.html')


def editProfile(request):
    obj = Account()
    authenticated = obj.get_userAuthenticated()
    if authenticated in "TRUE":
        allergies = loadAllergies()
        preferences = loadPreferences()
        if request.method == 'POST':
            acnt = Account()
            acnt.set_firstname(request.POST.get('firstname'))
            acnt.set_lastname(request.POST.get('lastname'))
            acnt.set_mobile(int(request.POST.get('phonenumber')))
            acnt.set_phone(int(request.POST.get('phonenumber')))
            acnt.updateUserAccount()
            user_info = obj.getUserAccount()
            address_info = obj.getUserAddress()
            return render(request, 'profile.html', {'check_list': allergies,'p_check_list': preferences ,'users': user_info,'addresses': address_info })
        else:
            user_info = obj.getUserAccount()
            address_info = obj.getUserAddress()
            return render(request, 'profile.html', {'check_list': allergies,'p_check_list': preferences ,'users': user_info,'addresses': address_info })
    else:
        return render(request,'login.html')

def editAddress(request):
    obj = Account()
    authenticated = obj.get_userAuthenticated()
    if authenticated in "TRUE":
        allergies = loadAllergies()
        preferences = loadPreferences()
        if request.method == 'POST':
            acnt = Account()
            acnt.set_addressName("Main")
            acnt.set_aptnum(request.POST.get('aptNum'))
            acnt.set_street(request.POST.get('street'))
            acnt.set_city(request.POST.get('city'))
            acnt.set_state(request.POST.get('state'))
            acnt.set_zipcode(int(request.POST.get('zip')))
            acnt.updateUserAddress("Main")
            user_info = obj.getUserAccount()
            address_info = obj.getUserAddress()
            return render(request, 'profile.html', {'check_list': allergies,'p_check_list': preferences ,'users': user_info,'addresses': address_info })
        else:
            user_info = obj.getUserAccount()
            address_info = obj.getUserAddress()
            return render(request, 'profile.html', {'check_list': allergies,'p_check_list': preferences ,'users': user_info,'addresses': address_info })
    else:
        return render(request,'login.html')

def customerAllergy(request):
    obj3 = Account()
    authenticated = obj3.get_userAuthenticated()
    if authenticated in "TRUE":  
        if request.method == 'POST': # If the form has been submitted...
            allergy_list = request.POST.getlist('a_checks[]')
            
            obj = Customer()
            customer_list = obj.viewAllergy()
            for allergy in allergy_list: #Find which prefrences have already been added and ignore 
                found = 0
                cus = Customer()
                for user_a in  customer_list:
                    if allergy in user_a:
                        found = 1
                        break
                if found == 0:
                    cus.set_allergy(allergy)
                    cus.addAllergy()
            for user_a in  customer_list:
                removed = 0
                for allergy in allergy_list:
                    if user_a in allergy :
                        removed = 1
                        break
                if removed == 0:
                    obj.set_allergy(user_a)
                    obj.removeAllergy()
            response = "Allergies are up-to-date" 
            allergies = loadAllergies()
            preferences = loadPreferences()
            context = {'response': response, 'check_list': allergies ,'p_check_list': preferences}
            return render(request, 'profile.html', context) # Redirect after POST
        else:
            allergies = loadAllergies()
            preferences = loadPreferences()
            return render(request, 'profile.html', {'check_list': allergies, 'p_check_list': preferences}) # Redirect 
    else:
            return render(request, 'login.html')    

def customerPreference(request):
    obj3 = Account()
    authenticated = obj3.get_userAuthenticated()
    if authenticated in "TRUE":  
        if request.method == 'POST': # If the form has been submitted...
            preference_list = request.POST.getlist('p_checks[]')
            obj = Customer()
            customer_list = obj.viewPreferences()
            for preference in preference_list:
                found = 0
                cus = Customer()
                for user_p in  customer_list:
                    if preference in user_p:
                        found = 1
                        break
                if found == 0:
                    cus.set_preference(preference) 
                    cus.addPreference()
            for user_p in  customer_list:
                removed_p = 0
                for preference in preference_list:
                    if user_p in preference :
                        removed_p = 1
                        break
                if removed_p == 0:
                    obj.set_preference(user_p)
                    obj.removePreference()
            response = "Preferences are up-to-date" 
            context = {'response': response}
            allergies = loadAllergies()
            preferences = loadPreferences()
            context = {'response': response, 'check_list': allergies ,'p_check_list': preferences}
            return render(request, 'profile.html', context) # Redirect after POST
        else:
            allergies = loadAllergies()
            preferences = loadPreferences()
            context = {'check_list': allergies ,'p_check_list': preferences}
            return render(request, 'profile.html', context)
    else:
        return render(request, 'login.html')
