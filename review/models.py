from django.db import models
from django.db import connection
from bearbites._con import getConnection
from bearbites._con import dictfetchall
from order.models import Delivery
# Create your models here.
class Review (Delivery):
    reviewID = models.IntegerField()
    reviewType = models.CharField(max_length=128)
    reviewRating = models.IntegerField()
    reviewComment = models.CharField()

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
