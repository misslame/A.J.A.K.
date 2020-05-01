from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from .models import Review
from bearbites.views import get_userinfo
from customer.views import lastOrder
from order.models import OrderHistory

# Create your views here.
def addReview(request):
    context = get_userinfo(request)
    if request.method == 'POST':
        feedback = Review()
        lastDelivery = OrderHistory()
        customerID = int(request.session['customer'])
        lastDelivery.set_customerID(customerID)
        delivID = int(lastDelivery.getLastOrder()) # Would Rather Get This from the Request if I can
        feedback.set_deliveryID(delivID)
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
        comments = request.POST.get('deliveryComment')
        if comments is None or len(comments) == 0:
            comments = ""
        feedback.set_reviewComment(comments)
        response = feedback.leaveReview()
        context.update({'response':response})
        context.update(lastOrder(request))
        return render(request,'profile.html',context)
    else:
        return render(request,'review.html',context)
