import re
from django.shortcuts import render
from django.http import HttpResponse
from .models import Account
from customer.views import loadAllergies, loadPreferences
from customer.models import Customer
from django.template import Context, loader



def indexView(request):
    obj = Account()
    obj.userAuthenticated.append("False")
    return render(request, 'index.html')
    

def dashboardView(request):
    return render(request,'index.html')

def registerView(request):
    if request.method == 'POST': # If the form has been submitted...
        valid = 0
        checkFields = []
        pas = request.POST.get('password')
        pas_c = request.POST.get('rpassword')
        email = request.POST.get('email')
        if pas == pas_c: #verify that both password and cormirmation field match
            valid = 1
            checkFields.append(" ")
        else:
            checkFields.append("Passwords do not match")
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if (re.search(regex,email)):
            valid += 1
            checkFields.append(" ")
        else:
            checkFields.append("Invalid Email Address")
        rules = [  #check that password has an upper and lower case letter as well as an number and 
        lambda pas: any(x.isupper() for x in pas) or 'upper',
        lambda pas: any(x.islower() for x in pas) or 'lower',
        lambda pas: any(x.isdigit() for x in pas) or 'digit',
        lambda pas: len(pas) >= 7                 or 'length',
        ]
        problems = [p for p in [r(pas) for r in rules] if p != True]
        if len(problems) ==0:
            checkFields.append(" ")
            valid += 1
        else:
            checkFields.append("Password does not meet security requirements")
        if valid == 3:
            obj = Account()
            obj.email.clear()
            obj.password.clear()
            obj.email.append(request.POST.get('email'))
            obj.password.append(request.POST.get('password'))
            obj.set_firstname(request.POST.get('firstname'))
            obj.set_lastname(request.POST.get('lastname'))
            obj.set_mobile(int(request.POST.get('phonenumber')))
            obj.set_phone(int(request.POST.get('phonenumber')))
            pas = request.POST.get('password')
            obj.set_email(request.POST.get('email'))
            obj.set_password(request.POST.get('password'))
            obj.set_addressName("Main")
            apt = request.POST.get('aptNum')
            print(apt)
            if len(apt) == 0:
                apt = " "
            obj.set_aptnum(apt)
            obj.set_street(request.POST.get('street'))
            obj.set_city(request.POST.get('city'))
            obj.set_state(request.POST.get('state'))
            obj.set_zipcode(int(request.POST.get('zip')))
            user = int(obj.addUserAccount())
            obj.set_accountID(int(user))
            obj.addAddress()
            response = obj.addCustomer()
            context = {'response': response}
            return render(request,'register.html', context)
        else:
            context = {'check_fields': checkFields}
            return render(request,'register.html', context)
    else :
        context = {'response': ""}
        return render(request,'register.html',context)

def loginView(request):
    if request.method == 'POST': # If the form has been submitted...
        
        obj = Account()
        obj.email.clear()
        obj.password.clear()
        obj.userAuthenticated.clear()
        obj.email.append(request.POST.get('email'))
        obj.password.append(request.POST.get('password'))
        row = obj.getUserAccount()
        print (row)
        if len(row) >0:
            user = obj.authenticateUser()
            obj.userAuthenticated.append("TRUE")
            obj.accountID.append(int(user[0]))
            obj.customerID.append(int(user[1]))
            cus = Customer()
            cus.accountID.clear()
            cus.customerID.clear()
            cus.customerID.append(int(user[1]))
            cus.accountID.append(int(user[0]))
            allergies = loadAllergies()
            preferences = loadPreferences()
            user_info = obj.getUserAccount()
            address_info = obj.getUserAddress()
            print(user_info)
            print(obj.get_accountID())
            return render(request,'profile.html',{'check_list': allergies,'p_check_list': preferences ,'users': user_info,'addresses': address_info })
        else:
            response = "Invalid Credentials, please try again!"
            obj.userAuthenticated.append("False")
            context = {'response': response}
            return render(request,'login.html',context)
    context = {'response': ""}
    return render(request,'login.html',context)

def profileView(request):

    return render(request,'profile.html')