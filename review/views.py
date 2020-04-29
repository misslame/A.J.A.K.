from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from .models import Review
from bearbites.views import get_userinfo

# Create your views here.
def addReviewView(request):
    context = get_userinfo(request)
    if request.method == 'POST':
        feedback = Review()
        feedback.set_deliveryID(request.POST.get('delivery'))
        feedback.set_customerID(int(request.session['customer']))
        feedback.set_reviewType(request.POST.get('type'))
        feedback.set_reviewRating(request.POST.get('rating'))
        comments = request.POST.get('comments')
        if comments is None or len(comments) == 0:
            comments = ""
        feedback.set_reviewComment(comments)
        response = feedback.leaveReview()
        context.update({'response':response})
        return render(request,'profile.html',context)
