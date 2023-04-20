from django.db import models
from django.contrib.auth.models import User

class Investor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def to_user(self):
        user, _ = User.objects.get_or_create(username=self.email)
        user.set_password(self.password)
        user.save()
        return user
