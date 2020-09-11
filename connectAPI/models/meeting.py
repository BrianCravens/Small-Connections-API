"""This file contains the Model for Meeting"""

from django.db import models
from .member import Member
from .group import Group

class Meeting(models.Model):

    """This class defines the Meeting for the Small Connections application"""

    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    member = models.ForeignKey(Member, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    content = models.TextField()
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)