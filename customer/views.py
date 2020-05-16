from django.shortcuts import render
from .models import Customer
from bearbites.models import Account
from order.models import OrderHistory



# Create your views here.

checkbox_list = ['Dairy', 'Eggs', 'Tree Nuts', 'Wheat', 'Peanuts', 'Soy','Fish','Shellfish']
p_checkbox_list = ['Diabetic', 'Gluten-Free', 'Vegetarian', 'Vegan', 'Pescetarian', 'Kosher','Paleo Diet','Mediterranean', 'Keto Diet', 'High Protein', 'Low Carb', 'Low Fat', 'Fast Food','Street Food','Fresh Food','Raw Food', 'Seafood','Sugar-Free','Low-Sodium','Low-Cholesterol','Organic', 'Non-GMO','Asian','African','American','Latin','European','Middle Eastern','Pacific']
def loadAllergies(request):
    obj = Customer()
    customerID = int(request.session['customer'])
    obj.set_customerID(customerID)
    print (obj.get_customerID())
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

def loadPreferences(request):
    obj = Customer()
    customerID = int(request.session['customer'])
    obj.set_customerID(customerID)
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

def get_userinfo(request):
    if 'name' in request.session:
        userInfo = request.session["name"]
        auth = True
        acnt = Customer()
        acnt.set_email(request.session['user'])
        acnt.set_password(request.session['password'])
        acnt.set_accountID(int(request.session['account']))
        acnt.set_customerID(int(request.session['customer']))
        user_info = acnt.getUserAccount()
        request.session['auth'] = True

    else:
        userInfo = ""
        user_info = ""
        auth = False
        request.session['auth'] = False
    dict = {'authenticated_user':userInfo,'userauthenticated':auth,'users': user_info}
    return   dict

def lastOrder(request):
    previous = OrderHistory()
    previous.set_customerID(int(request.session.get('customer')))
    last = previous.getLastOrder() # Returns Last Order info
    return last


def loadOrderHistory(request):
    history = OrderHistory()
    history.set_customerID(int(request.session.get('customer')))
    Ohistory = history.getAllOrderDetail()
    return Ohistory
    
def loadProfile(request):
    obj = Customer()
    if 'auth' in request.session:
        authenticated = request.session['auth']
    else:
        authenticated = False

    if authenticated == True:
        allergies = loadAllergies(request)
        preferences = loadPreferences(request)
        obj.set_email(request.session['user'])
        obj.set_password(request.session['password'])
        obj.set_accountID(int(request.session['account']))
        obj.set_customerID(int(request.session['customer']))
        user_info = obj.getUserAccount()
        address_info = obj.view_userAddresses()
        print(user_info)
        print(obj.get_accountID())
        context = get_userinfo(request)
        lstOrder = lastOrder(request)
        history=[]
        reviews=[]
        if len(lstOrder) != 0:
            history = loadOrderHistory(request)
            reviews = obj.view_UserReviews()
        context.update({'lastOrder':lstOrder,'history':history,'check_list': allergies,'p_check_list': preferences ,'users': user_info,'addresses': address_info , 'reviews':reviews})
        return render(request, 'profile.html',context)
    else:
        return render(request,'login.html')



def editProfile(request):
    if 'auth' in request.session:
        authenticated = request.session['auth']
    else:
        authenticated = False

    if authenticated == True:
        allergies = loadAllergies(request)
        preferences = loadPreferences(request)
        acnt = Customer()
        acnt.set_email(request.session['user'])
        acnt.set_password(request.session['password'])
        acnt.set_accountID(int(request.session['account']))
        acnt.set_customerID(int(request.session['customer']))
        context = get_userinfo(request)

        if request.method == 'POST':
            acnt.set_firstname(request.POST.get('firstname'))
            acnt.set_lastname(request.POST.get('lastname'))
            acnt.set_mobile(int(request.POST.get('phonenumber')))
            acnt.set_phone(int(request.POST.get('phonenumber')))
            acnt.updateUserAccount()
            user_info = acnt.getUserAccount()
            address_info = acnt.view_userAddresses()
            user = acnt.authenticateCustomer()
            name = user[2]
            request.session["name"] = name
            context = get_userinfo(request)
            lstOrder = lastOrder(request)
            history=[]
            reviews=[]
            if len(lstOrder) != 0:
                history = loadOrderHistory(request)
                reviews = acnt.view_UserReviews()
            context.update({'lastOrder':lstOrder,'history':history,'check_list': allergies,'p_check_list': preferences ,'users': user_info,'addresses': address_info , 'reviews':reviews})
            return render(request, 'profile.html',context )
        else:
            lstOrder = lastOrder(request)
            history=[]
            reviews=[]
            user_info = acnt.getUserAccount()
            address_info = acnt.view_userAddresses()
            if len(lstOrder) != 0:
                history = loadOrderHistory(request)
                reviews = acnt.view_UserReviews()
            context.update({'lastOrder':lstOrder,'history':history,'check_list': allergies,'p_check_list': preferences ,'users': user_info,'addresses': address_info , 'reviews':reviews})
            return render(request, 'profile.html', context)
    else:
        return render(request,'login.html')

def editAddress(request):
    acnt = Customer()
    if 'auth' in request.session:
        authenticated = request.session['auth']
    else:
        authenticated = False

    if authenticated == True:
        allergies = loadAllergies(request)
        preferences = loadPreferences(request)
        acnt.set_email(request.session['user'])
        acnt.set_password(request.session['password'])
        acnt.set_accountID(int(request.session['account']))
        acnt.set_customerID(int(request.session['customer']))
        context = get_userinfo(request)
        if request.method == 'POST':
            selectedAdd = request.POST.get('selectaddress')
            apt = request.POST.get('apt '+selectedAdd)
            if len(apt) == 0:
                apt = " "
            acnt.set_addressName(selectedAdd)
            acnt.set_aptnum(apt)
            acnt.set_street(request.POST.get('street '+selectedAdd))
            acnt.set_city(request.POST.get('city '+selectedAdd))
            acnt.set_state(request.POST.get('state '+selectedAdd))
            acnt.set_zipcode(int(request.POST.get('zip '+selectedAdd)))
            addressName = request.POST.get('addName '+selectedAdd)
            acnt.set_addressName(selectedAdd)
            
            if 'new' in selectedAdd :
                acnt.set_addressName(addressName)
                acnt.addAddress()
            else:
                acnt.set_addressName(selectedAdd)
                acnt.updateUserAddress(selectedAdd)
            address_info = acnt.view_userAddresses()
            lstOrder = lastOrder(request)
            history=[]
            reviews=[]
            if len(lstOrder) != 0:
                history = loadOrderHistory(request)
                reviews = acnt.view_UserReviews()
            context.update({'lastOrder':lstOrder,'history':history,'check_list': allergies,'p_check_list': preferences ,'addresses': address_info , 'reviews':reviews})
            return render(request, 'profile.html', context)
        else:
            address_info = acnt.view_userAddresses()
            lstOrder = lastOrder(request)
            history=[]
            reviews=[]
            if len(lstOrder) != 0:
                history = loadOrderHistory(request)
                reviews = acnt.view_UserReviews()
            context.update({'lastOrder':lstOrder,'history':history,'check_list': allergies,'p_check_list': preferences ,'addresses': address_info , 'reviews':reviews})
            return render(request, 'profile.html', context)
    else:
        return render(request,'login.html')

def customerAllergy(request):

    if 'auth' in request.session:
        authenticated = request.session['auth']
    else:
        authenticated = False

    if authenticated == True:
        obj = Customer()
        obj.set_email(request.session['user'])
        obj.set_password(request.session['password'])
        obj.set_accountID(int(request.session['account']))
        obj.set_customerID(int(request.session['customer']))
        context = get_userinfo(request)
        if request.method == 'POST': # If the form has been submitted...
            allergy_list = request.POST.getlist('a_checks[]')
            customer_list = obj.viewAllergy()
            for allergy in allergy_list: #Find which prefrences have already been added and ignore
                found = 0
                for user_a in  customer_list:
                    if allergy in user_a:
                        found = 1
                        break
                if found == 0:
                    obj.set_allergy(allergy)
                    obj.addAllergy()
            for user_a in  customer_list:
                removed = 0
                for allergy in allergy_list:
                    if user_a in allergy :
                        removed = 1
                        break
                if removed == 0:
                    obj.set_allergy(user_a)
                    obj.removeAllergy()
            user_info = obj.getUserAccount()
            address_info = obj.view_userAddresses()
            response = "Allergies are up-to-date"
            allergies = loadAllergies(request)
            preferences = loadPreferences(request)
            lstOrder = lastOrder(request)
            history=[]
            reviews=[]
            if len(lstOrder) != 0:
                history = loadOrderHistory(request)
                reviews = obj.view_UserReviews()
            context.update({'response':response,'lastOrder':lstOrder,'history':history,'check_list': allergies,'p_check_list': preferences ,'users': user_info,'addresses': address_info , 'reviews':reviews})
            return render(request, 'profile.html', context) # Redirect after POST
        else:
            allergies = loadAllergies(request)
            preferences = loadPreferences(request)
            user_info = obj.getUserAccount()
            address_info = obj.view_userAddresses()
            lstOrder = lastOrder(request)
            history=[]
            reviews=[]
            if len(lstOrder) != 0:
                history = loadOrderHistory(request)
                reviews = obj.view_UserReviews()
            context.update({'lastOrder':lstOrder,'history':history,'check_list': allergies,'p_check_list': preferences ,'users': user_info,'addresses': address_info , 'reviews':reviews})
            return render(request, 'profile.html', context) # Redirect
    else:
        return render(request, 'login.html')

def customerPreference(request):
    if 'auth' in request.session:
        authenticated = request.session['auth']
    else:
        authenticated = False

    if authenticated == True:
        obj = Customer()
        obj.set_email(request.session['user'])
        obj.set_password(request.session['password'])
        obj.set_accountID(int(request.session['account']))
        obj.set_customerID(int(request.session['customer']))
        context = get_userinfo(request)
        if request.method == 'POST': # If the form has been submitted...
            preference_list = request.POST.getlist('p_checks[]')
            customer_list = obj.viewPreferences()
            for preference in preference_list:
                found = 0
                for user_p in  customer_list:
                    if preference in user_p:
                        found = 1
                        break
                if found == 0:
                    obj.set_preference(preference)
                    obj.addPreference()
            for user_p in  customer_list:
                removed_p = 0
                for preference in preference_list:
                    if user_p in preference :
                        removed_p = 1
                        break
                if removed_p == 0:
                    obj.set_preference(user_p)
                    obj.removePreference()
            user_info = obj.getUserAccount()
            address_info = obj.view_userAddresses()
            context = get_userinfo(request)
            allergies = loadAllergies(request)
            preferences = loadPreferences(request)
            response = "User preferences have been updated"
            lstOrder = lastOrder(request)
            history=[]
            reviews=[]
            if len(lstOrder) != 0:
                history = loadOrderHistory(request)
                reviews = obj.view_UserReviews()
            
            context.update({'reviews':reviews,'response': response, 'lastOrder':lstOrder,'history': history,'check_list': allergies ,'p_check_list': preferences,'addresses': address_info})

            return render(request, 'profile.html', context) # Redirect after POST
        else:
            allergies = loadAllergies(request)
            preferences = loadPreferences(request)
            user_info = obj.getUserAccount()
            address_info = obj.view_userAddresses()
            lstOrder = lastOrder(request)
            history=[]
            reviews=[]
            response = "Not updated"
            if len(lstOrder) != 0:
                history = loadOrderHistory(request)
                reviews = obj.view_UserReviews()
            context.update({'reviews':reviews,'response': response, 'lastOrder':lstOrder,'history': history,'check_list': allergies ,'p_check_list': preferences,'addresses': address_info})
            return render(request, 'profile.html', context)
    else:
        return render(request, 'login.html')

def loadCustomerReviews(request):
    obj = Customer()
    if 'auth' in request.session:
        authenticated = request.session['auth']
    else:
        authenticated = False

    if authenticated == True:
        allergies = loadAllergies(request)
        preferences = loadPreferences(request)
        obj.set_email(request.session['user'])
        obj.set_password(request.session['password'])
        obj.set_accountID(int(request.session['account']))
        obj.set_customerID(int(request.session['customer']))
        user_info = obj.getUserAccount()
        address_info = obj.view_userAddresses()
        context = get_userinfo(request)
        lstOrder = lastOrder(request)
        history=[]
        reviews=[]
        if len(lstOrder) != 0:
            history = loadOrderHistory(request)
            reviews = obj.view_UserReviews()
            
        context.update({'reviews':reviews, 'lastOrder':lstOrder,'history': history,'check_list': allergies ,'p_check_list': preferences,'addresses': address_info})
        return render(request, 'profile.html',context)
    else:
        return render(request,'login.html')

