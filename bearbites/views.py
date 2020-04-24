import re
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from .models import Account
from customer.views import loadAllergies, loadPreferences, get_userinfo
from order.views import lastOrder
from customer.models import Customer
from django.template import Context, loader



def indexView(request):
    context = get_userinfo(request)
    return render(request, 'index.html',context)


def dashboardView(request):
    return render(request,'index.html')

def trialDashBoardView(request):
    context = get_userinfo(request)
    context.update(lastOrder(request))
    print("\n\n")
    print(context)
    print("\n\n")
    return render(request, 'trial_dashboard.html',context)

def orderView(request):
    return render(request, 'order.html')


def registerView(request):
    if request.method == 'POST': # If the form has been submitted..
        valid = 0
        checkFields = []
        formFields = [] #save form fields
        formFields.append(request.POST.get('firstname'))
        formFields.append(request.POST.get('lastname'))
        formFields.append(request.POST.get('phonenumber'))
        formFields.append(request.POST.get('email'))
        formFields.append(request.POST.get('password'))
        formFields.append(request.POST.get('rpassword'))
        formFields.append(request.POST.get('aptNum'))
        formFields.append(request.POST.get('street'))
        formFields.append(request.POST.get('city'))
        formFields.append(request.POST.get('state'))
        formFields.append(request.POST.get('zip'))

        pas = request.POST.get('password')
        pas_c = request.POST.get('rpassword')
        email = request.POST.get('email')
        if pas == pas_c: #verify that both password and confirmation field match
            valid = 1
            checkFields.append(" ")
        else:
            checkFields.append("Passwords do not match")
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        obj = Customer()
        if (re.search(regex,email)):
            if obj.checkEmailExists(email)== False:
                valid += 1
                checkFields.append(" ")
            else:
                checkFields.append("An account with this email exsists already")
        else:
            checkFields.append("Invalid Email Address please enter a valid email")
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
        check_term = request.POST.getlist('termcond')
        if len(check_term) ==1:
            checkFields.append(" ")
            valid += 1
        else:
            checkFields.append("Please accept terms and conditions!")
        if valid == 4:

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
            context = {'response': response, 'alert_flag': True}

            return render(request,'register.html', context)
        else:
            response = "There was an error creating the account. Please see the fields below."
            context = {'response': response,'check_fields': checkFields,'form_fields': formFields, 'alert_flag': True}

            return render(request,'register.html',context)
    else :
        context = {'response': ""}
        return render(request,'register.html',context)


def loginView(request):

    if request.method == 'POST': # If the form has been submitted...
        obj = Customer()
        email = request.POST.get('email')
        password = request.POST.get('password')
        if len(email)== 0 or len(password)== 0:
            row = ""
        else:
            obj.set_email(email)
            obj.set_password(password)
            row = obj.getUserAccount()

        print (row)
        if len(row) >0:
            user = obj.authenticateCustomer()
            request.session["user"] = email
            request.session["password"] = password
            request.session["auth"] = True
            request.session["account"] = int(user[0])
            request.session["customer"] = int(user[1])
            obj.set_accountID(int(user[0]))
            obj.set_customerID(int(user[1]))
            allergies = loadAllergies(request)
            preferences = loadPreferences(request)
            user_info = obj.getUserAccount()
            address_info = obj.getUserAddress()
            state =[ sub['state'] for sub in address_info ]
            name = user[2]
            request.session["name"] = name
            print(request.session["name"])
            context = get_userinfo(request)
            context.update({'check_list': allergies,'p_check_list': preferences ,'users': user_info,'addresses': address_info ,'state':state})
            return render(request,'profile.html',context)
        else:
            response = "Invalid Credentials, please try again!"
            obj.set_userAuthenticated(False)
            context = {'response': response, 'alert_flag': True}
            return render(request,'login.html',context)
    context = {'response': ""}
    return render(request,'login.html',context)


def logout(request):
    try:
        del request.session["user"]
        del request.session["name"]
        del request.session["password"]
        del request.session["auth"]
        del request.session["account"]
        del request.session["customer"]
    except:
        return HttpResponse("<h1>dataflair<br>Session Data not cleared</h1>")
    request.session.modified = True
    return redirect('/login')

def profileView(request):
    return render(request,'profile.html')
