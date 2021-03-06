"""This file contains the Model for Member"""

from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

class Member(models.Model):

    """This is the class that defines the Member Model for the Small Connections application"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=95, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    image = models.CharField(max_length=255,blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = ("Member")
        verbose_name_plural = ("Members")

    def get_absolute_url(self):
        return reverse("Member_detail", kwargs={"pk": self.pk})