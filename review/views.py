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
        order = request.COOKIES['order']#get cart items
        customerID = int(request.session['customer'])
        lastDelivery.set_customerID(customerID)
        feedback.set_deliveryID(int(order))
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

## Review for Delivery Driver
        feedback.set_reviewType('Delivery')
        rating=request.POST.get('deliveryReview')
        feedback.set_reviewRating(rating)
        comments = request.POST.get('deliveryComment')
        if comments is None or len(comments) == 0:
            comments = ""
        feedback.set_reviewComment(comments)
        response = feedback.leaveReview()
        context.update({'response':response,'alert_flag': True})
        context.update(lastOrder(request))
        
        context.update(loadOrderHistory(request))
        return render(request,'profile.html',context)
    else:
        return render(request,'review.html',context)

