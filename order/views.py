from django.shortcuts import render
from .models import OrderHistory
from customer.views import get_userinfo
from datetime import datetime as dt
from bearbites.models import Account
from restaurant.models import Restaurant
from menu.models import Menu, MenuItem
import json
import ast
import html
from urllib.parse import unquote



# Create your views here.

def CreateOrder(request):
    if request.method == 'POST':
        cartitems = request.COOKIES['cart']#get cart items
        decode = unquote(str(cartitems)) #decode the url
        cart = ast.literal_eval(decode)#read the string as a dict
        print ('printing sorted cart')
        sorted_cart = []
        sorted_cart = sorted(cart, key = lambda i: i['restaurantID']) #sort cart items by restaurant
        
        order = OrderHistory()
        apt = request.POST.get('apt')
        if len(apt) == 0:
            apt = " "
        order.set_aptnum(apt)
        street = request.POST.get('street')
        order.set_street(street)
        city = request.POST.get('city')
        order.set_city(city)
        state = request.POST.get('state')
        order.set_state(state)
        zipcode = request.POST.get('zip')
        cardnum = str(request.POST.get('cardnum'))
        cardFormat = "".join(['#' for x in cardnum[:-4]]) + cardnum[-4:]


        cardowner = request.POST.get('cardowner')
        order.set_zipcode(int(zipcode))
        now = dt.now()
        order.set_deliveryTime(now.strftime("%H:%M:%S"))
        order.set_deliveryDate(now.strftime("%m/%d/%Y"))
        order.set_customerID(int(request.session['customer']))
        order.set_accountID(int(request.session['account']))
        addressID = int(order.get_AddressID())
        order.set_deliveryAddressID(addressID)
        tip = request.POST.get('tip')
        order.set_tip(tip)
        instructions = request.POST.get('DeliveryInstructions')
        order.set_deliveryInstructions(instructions)
        previous = 0
        Restaurantid = 0
        total = 0.0
        subtotal = 0.0
        itemPrice = 0.0
        quan = 0
        for itm in sorted_cart:
            carti = itm
            for key in carti.keys():
                if key == 'id':
                    print(str(carti[key]))
                    order.set_itemID(int(carti[key]))
                    itemPrice = order.getItemPrice()
                    Restaurantid = int(order.getItemRestaurant())
             
                elif key =='quantity': 
                    quan = int(carti[key])  
                    order.set_quantity(int(quan))
                    newitemPrice = float(itemPrice) * float(quan)
                    subtotal += newitemPrice
                elif key == 'price':
                    carti[key] = "{:.2f}".format(newitemPrice)

                elif key == 'instructions':
                    order.set_specialInstructions(str(carti[key])) 

                elif key == 'restaurantID':
                    rest = int(Restaurantid)
                    if rest != previous: #check if item belongs to the same restaurant
                        
                        order.set_restaurant(int(Restaurantid))
                        order.set_deliveryID(int(order.processDelivery()))
                    cartID= order.addToCart()
                    order.set_cartItemID(cartID)
                    order.createOrder()
                    previous = rest
        tax = subtotal * 0.05
        response = "Your order has been placed and will be there shortly!"
        print(response)
        formatted_subtotal = "{:.2f}".format(subtotal)
        formatted_tax = "{:.2f}".format(tax)
        total = subtotal+ float(formatted_tax) + float(tip)
        
        formatted_total = "{:.2f}".format(total)
        context = get_userinfo(request)
        context.update({ 'response':response,'cart':cart,'total':formatted_total,'tip': tip,'tax':formatted_tax,'subtotal':formatted_subtotal,'city':city, 'state':state, 'apt':apt,'street':street,'zip':zipcode, 'CardOwner': cardowner,'card':cardFormat, 'instructions':instructions})
        return render(request,'order_confirmation.html',context)
       
    context = get_userinfo(request)
    obj = OrderHistory()
    obj.set_accountID(int(request.session['account']))
    address_info = obj.getUserAddress()
    cartitems = request.COOKIES['cart']#get cart items
    decode = unquote(str(cartitems)) #decode the url
    cart= ast.literal_eval(decode)#read the string as a dict
    total = 0.0
    subtotal = 0.0
    itemPrice = 0.0
    for itm in cart:
        carti = itm
        for key in carti.keys():
            if key == 'id':
                print(str(carti[key]))
                obj.set_itemID(int(carti[key]))
                itemPrice = obj.getItemPrice()
            if key =='quantity': 
                print(str(carti[key]))   
                newitemPrice = float(itemPrice) * float(carti[key])
                subtotal += newitemPrice
            if key == 'price':
                carti[key] = "{:.2f}".format(newitemPrice)
    tax = subtotal * 0.05
    formatted_subtotal = "{:.2f}".format(subtotal)
    formatted_tax = "{:.2f}".format(tax)
    total = subtotal+ float(formatted_tax)
    formatted_total = total *100
    formatted_total = formatted_total/100.0
    formatted_total = "{:.2f}".format(total)
    context.update({'addresses':address_info, 'cart':cart,'total':formatted_total,'tax':formatted_tax,'subtotal':formatted_subtotal})
    return render(request,'cart.html',context)

        

