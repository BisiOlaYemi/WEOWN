from django.db import models
from django.db import models

class Investor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    pr_status = models.CharField(max_length=100)
    credit_score = models.IntegerField()
    address = models.CharField(max_length=200)
    current_location = models.CharField(max_length=200)
