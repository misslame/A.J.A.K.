from django.shortcuts import render
from .models import OrderHistory
from customer.views import get_userinfo
from datetime import datetime as dt
from bearbites.models import Account
from restaurant.models import Restaurant
from menu.models import Menu, MenuItem


# Create your views here.

def CreateOrder(request):
    if request.method == 'POST':
        order = OrderHistory()
        apt = request.POST.get('apt')
        if len(apt) == 0:
            apt = " "
        order.set_aptnum(apt)
        order.set_street(request.POST.get('street'))
        order.set_city(request.POST.get('city'))
        order.set_state(request.POST.get('state'))
        order.set_zipcode(int(request.POST.get('zip')))
        now = dt.now()
        order.set_deliveryTime(now.strftime("%H:%M:%S"))
        order.set_deliveryDate(now.strftime("%m/%d/%Y"))
        order.set_customerID(int(request.session['customer']))
        order.set_accountID(int(request.session['account']))
        addressID = int(order.get_AddressID())
        order.set_deliveryAddressID(addressID)
        order.set_restaurant(int(request.POST.get('restaurantID')))
        order.set_deliveryID(int(order.processDelivery()))

        items_list = request.POST.getlist('cart_items[]')
        for item in items_list:
            order.set_itemID(item)
            order.set_quantity(1)
            order.set_specialInstructions(request.POST.get('specialInstructions'))
            cartID= order.addToCart()
            order.set_cartItemID(cartID)
            order.createOrder()
        context = get_userinfo(request)
        response = "Your order has been placed and will be there shortly!"
        target = Restaurant()
        restaurants = target.view_AllRestaurants()
        context.update({'response': response,'restaurants':restaurants, 'alert_flag': True})
        return render(request, 'locations.html',context) # Changed JDR
    menuIt = MenuItem()
    restaurantID = request.GET['pk']
    # print(str(restaurantID))
    menuIt.set_restaurantID(int(restaurantID))
    menuItems = menuIt.viewItems()
    restaurantInfo =  menuIt.viewRestaurant()
    context = get_userinfo(request)
    obj = Account()
    obj.set_accountID(int(request.session['account']))
    address_info = obj.getUserAddress()
    context.update({'menuitems':menuItems,'restaurantInfo':restaurantInfo,'addresses':address_info,'restaurant':restaurantID})
    return render(request,'order.html',context) # Changed JDR

def lastOrder(request):
    previous = OrderHistory()
    previous.set_customerID(int(request.session.get('customer')))
    last = previous.getLastOrder() # Returns Last Order's Delivert ID
    previous.set_deliveryID(last)
    delivery_info = previous.checkDeliveryInfo() # Returns dictfetchall of Delivery row
    previous.set_deliveryAddressID(delivery_info[0]["DeliveryAddressID"])
    orderDate = delivery_info[0]["DeliveryDate"]
    orderTime = delivery_info[0]["DeliveryTime"]
    previous.set_deliveryDate(orderDate)
    previous.set_deliveryTime(orderTime)
    recent_restaurants = previous.getOrderRestaurants() #Returns 1D list of Restaurant names
    delivery_address = previous.get_AddressDetails()
    last_order = {
        "orderDate": orderDate,
        "orderTime": orderTime,
        "recent_restaurants": recent_restaurants,
        "delivery_address": delivery_address
    }
    return last_order

def orderHistory(request):
    review = OrderHistory()
    review.set_customerID(int(request.session.get('customer')))
    last = review.getLastOrder()
    print("last order is " + str(last))
    review.set_deliveryID(last)
    delivery_info = review.checkDeliveryInfo()
    review.set_deliveryAddressID(delivery_info[0]["DeliveryAddressID"])
    allDeliveries = review.findConcurrentDeliveries()
    delivery_address = review.get_AddressDetails()
    picnic_basket ={}
    for delivery in allDeliveries:
        review.set_deliveryID(int(delivery))
        basket = review.getCartItems()
        for item in basket:
            review.set_cartItemID(int(item))
            cartDetails = review.getCartDetails()
            review.set_itemID(int(review.findInMenu()))
            itemDetails = review.foodForensics() #Trace an itemID to its restaurant name, item name, and item details
            restaurantName = itemDetails[0]["restaurantName"]
            del itemDetails[0]["restaurantName"]
            itemDetails[0].update(cartDetails)
            # print("\n\n\n")
            # print(itemDetails[0])
            # print("\n\n\n")
            if restaurantName not in picnic_basket:
                # print("{} is not in the dictionary".format(restaurantName))
                picnic_basket[restaurantName] = list()
            # print(picnic_basket[restaurantName])
            # print(type(picnic_basket[restaurantName]))
            picnic_basket[restaurantName] = [*picnic_basket[restaurantName],itemDetails[0]]
    # print(picnic_basket)
    context = get_userinfo(request)
    context.update({'orders':picnic_basket})
    return context
