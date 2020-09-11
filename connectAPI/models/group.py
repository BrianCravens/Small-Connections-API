"""This file contains the Model for Group"""

from django.db import models
from .member import Member

class Group(models.Model):

    """This class defines the Group for the Small Connections application"""

    leader = models.ForeignKey(Member, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=25)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=15)
    capacity = models.IntegerField()
    schedule = models.CharField(max_length=50)
    image = models.ImageField()
    kids = models.BooleanField(default=False)
