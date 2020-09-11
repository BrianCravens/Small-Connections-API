"""This file contains the Model for Member Group"""

from django.db import models
from .member import Member
from .group import Group

class MemberGroup(models.Model):

    """This class defines the Member Group for the Small Connections application"""

    member = models.ForeignKey(Member, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    is_approved = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)