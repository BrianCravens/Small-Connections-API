"""This file contains the Model for Prayer"""

from django.db import models
from .member import Member
from .group import Group

class Prayer(models.Model):

    """This class defines the Prayer for the Small Connections application"""

    member = models.ForeignKey(Member, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)