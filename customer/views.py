from django.shortcuts import render
from .models import Customer
from bearbites.models import Account
# Create your views here.
cus_id = 1
checkbox_list = ['Milk', 'Eggs', 'True Nuts', 'Wheat', 'Peanuts', 'Soy','Fish','ShellFish']
p_checkbox_list = ['Diabetic', 'Gluten-Free', 'Vegetarian', 'Vegan', 'Pescatarian', 'Kosher','Paleo Diet','Mediterranean Diet', 'Keto Diet', 'High Protein', 'Low Carb', 'Low Fat', 'Raw Food', 'Fast Food','Street Food','Fresh Food', 'Seafood','Sugar-Free','Low-Sodium','Low-Cholesterol','Organic', 'Non-GMO','Asian','African','American','Latin','European','Middle Eastern','Pasific']
def loadAllergies():
    obj = Customer()
    obj.set_customerID(cus_id)
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
    obj.set_customerID(cus_id)
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
    allergies = loadAllergies()
    preferences = loadPreferences()
    obj = Account()
    obj.set_email("juliethjar@misena.edu.co") #replace with current value of autherized user
    obj.set_password("newtespass") #replace with current value of autherized user
    userID = 14 #replace with current value of autherized user
    obj.set_user(userID)
    user_info = obj.getUserAccount()
    address_info = obj.getUserAddress()
    return render(request, 'profile.html', {'check_list': allergies,'p_check_list': preferences ,'users': user_info,'addresses': address_info })

def editProfile(request):
    allergies = loadAllergies()
    preferences = loadPreferences()
    obj = Account()
    obj.set_email("juliethjar@misena.edu.co") #replace with current value of autherized user
    obj.set_password("newtespass") #replace with current value of autherized user
    userID = 14 #replace with current value of autherized user
    obj.set_user(userID)
    if request.method == 'POST':
        acnt = Account()
        acnt.set_firstname(request.POST.get('firstname'))
        acnt.set_lastname(request.POST.get('lastname'))
        acnt.set_mobile(int(request.POST.get('phonenumber')))
        acnt.set_phone(int(request.POST.get('phonenumber')))
        acnt.set_email(request.POST.get('email'))
        acnt.updateUserAccount(userID)
        user_info = obj.getUserAccount()
        address_info = obj.getUserAddress()
        return render(request, 'profile.html', {'check_list': allergies,'p_check_list': preferences ,'users': user_info,'addresses': address_info })
    else:
        user_info = obj.getUserAccount()
        address_info = obj.getUserAddress()
        return render(request, 'profile.html', {'check_list': allergies,'p_check_list': preferences ,'users': user_info,'addresses': address_info })


def editAddress(request):
    allergies = loadAllergies()
    preferences = loadPreferences()
    obj = Account()
    obj.set_email("juliethjar@misena.edu.co") #replace with current value of autherized user
    obj.set_password("newtespass") #replace with current value of autherized user
    userID = 14 #replace with current value of autherized user
    obj.set_user(userID)
    if request.method == 'POST':
        acnt = Account()
        acnt.set_addressName("Main")
        acnt.set_aptnum(request.POST.get('aptNum'))
        acnt.set_street(request.POST.get('street'))
        acnt.set_city(request.POST.get('city'))
        acnt.set_state(request.POST.get('state'))
        acnt.set_zipcode(int(request.POST.get('zip')))
        acnt.updateUserAddress(userID,"Main")
        user_info = obj.getUserAccount()
        address_info = obj.getUserAddress()
        return render(request, 'profile.html', {'check_list': allergies,'p_check_list': preferences ,'users': user_info,'addresses': address_info })
    else:
        user_info = obj.getUserAccount()
        address_info = obj.getUserAddress()
        return render(request, 'profile.html', {'check_list': allergies,'p_check_list': preferences ,'users': user_info,'addresses': address_info })


def customerAllergy(request):  
    if request.method == 'POST': # If the form has been submitted...
        cus_id = 1 # using 1 as a filler until login is done and we get customerid
        allergy_list = request.POST.getlist('a_checks[]')
        
        obj = Customer()
        obj.set_customerID(cus_id)
        customer_list = obj.viewAllergy()
        for allergy in allergy_list:
            found = 0
            cus = Customer()
            cus.set_customerID(cus_id)
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
        

def customerPreference(request):
    if request.method == 'POST': # If the form has been submitted...
        cus_id = 1 
        preference_list = request.POST.getlist('p_checks[]')
        obj = Customer()
        obj.set_customerID(cus_id)
        customer_list = obj.viewPreferences()
        for preference in preference_list:
            found = 0
            cus = Customer()
            cus.set_customerID(cus_id) # using 1 as a filler until login is done and we get customerid
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