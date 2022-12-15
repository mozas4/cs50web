from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=64)
    des = models.TextField()
    bid = models.IntegerField(default=0)
    url = models.CharField(max_length=64)
    category = models.CharField(max_length=10) 

    def __str__(self):
        return f"listing of {self.title} belongs to {self.owner}"
