from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing():
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=64)
    des = models.CharField()
    bid = models.IntegerField()
    url = models.CharField()
    category = models.CharField() 

    def __str__(self):
        return f"listing of {self.title} belongs to {self.owner}"