from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from .models import Review
from bearbites.views import get_userinfo
from customer.views import lastOrder, loadOrderHistory
from order.models import OrderHistory

# Create your views here.
def addReview(request):
    context = get_userinfo(request)
    if request.method == 'POST':
        feedback = Review()
        lastDelivery = OrderHistory()
        order = request.COOKIES.get('order', None)#get cart items
        #order = [{"id":"15","name":"Strawberry Swirl Cheesecake","quantity":"1","price":"3.3500","instructions":"use stevia","restaurantID":"1"},{"id":"14","name":"Loaded Breakfast Burrito","quantity":"1","price":"5.1900","instructions":"low fat","restaurantID":"1"}]
        
        customerID = int(request.session['customer'])
        lastDelivery.set_customerID(customerID)
        feedback.set_deliveryID(1) # 1 = int(order)
        feedback.set_customerID(customerID)
        
        ## Review For Restaurant
        feedback.set_reviewType('Restaurant')
        rating = request.POST.get('restaurantReview')
        feedback.set_reviewRating(rating)
        comments = request.POST.get('restaurantComment')
        if comments is None or len(comments) == 0:
            comments = ""
        feedback.set_reviewComment(comments)
        feedback.leaveReview()

        # Review for Delivery Driver
        feedback.set_reviewType('Delivery')
        rating=request.POST.get('deliveryReview')
        feedback.set_reviewRating(rating)
        comments = request.POST.get('deliveryComment')
        if comments is None or len(comments) == 0:
            comments = ""
        feedback.set_reviewComment(comments)
        response = feedback.leaveReview()
        lstOrder = lastOrder(request)
        hist = loadOrderHistory(request)
        reviews = feedback.view_UserReviews()
        context.update({'lastOrder':lstOrder,'history':hist,'reviews':reviews,'response':response,'alert_flag': True})
        return render(request,'profile.html',context)
    else:
        return render(request,'review.html',context)

