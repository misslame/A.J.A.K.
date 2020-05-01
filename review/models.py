from django.db import models
from django.db import connection
from bearbites._con import getConnection
from bearbites._con import dictfetchall
from order.models import Delivery
# Create your models here.

class Review (Delivery):
    reviewID = models.IntegerField()
    reviewType = models.CharField(max_length=128)
    reviewRating = models.CharField(max_length=128)
    reviewComment = models.CharField(max_length=128)

# Getter Methods
    def __str__(self):
        return self.reviewComment

    def get_reviewID(self):
        return self.reviewID

    def get_reviewType(self):
        return self.reviewType

    def get_reviewRating(self):
        return self.reviewRating

    def get_reviewComment(self):
        return self.reviewComment

# Setter Methods
    def set_reviewID(self,num):
        self.reviewID = num

    def set_reviewType(self,type):
        self.reviewType = type

    def set_reviewRating(self,stars):
        self.reviewRating = stars

    def set_reviewComment(self,feedback):
        self.reviewComment = feedback

## Database Queries

# Write a Review
    def leaveReview(self):
        try:
            cnxn = getConnection()
            cursor = cnxn.cursor()
            sql = ("INSERT INTO Reviews(DeliveryID, CustomerID, ReviewType, ReviewRating, ReviewComment)"
                    " VALUES ({}, {}, '{}', '{}', '{}');").format(int(self.deliveryID),int(self.customerID),self.reviewType, self.reviewRating, self.reviewComment)
            cursor.execute(sql)
            cnxn.commit()
            cursor.close()
            cnxn.close()
            del cnxn
            response = "Review Placed"
        except:
            response = "Error Leaving Review"
        return response
