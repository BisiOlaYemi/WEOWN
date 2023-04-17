from django.db import models

class Investor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
