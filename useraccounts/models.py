from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=False, blank=False,
        related_name='profile', related_query_name='profile'
    )
    tax_identification_number = models.CharField(max_length=15)
    country = CountryField(default='AR')

    def __str__(self):
        return '{username}'.format(username=self.user.username.capitalize())

    class Meta:
        app_label = 'auth'


class UserRole(models.Model):
    # CST MNF PRV SLR
    id = models.CharField(max_length=3, primary_key=True, editable=False)
    description = models.CharField(max_length=60)

    def __str__(self):
        return '{description}({id})'.format(description=_(self.description), id=self.id)


class UserAddress(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=False, blank=False, related_name='address'
    )
    street = models.CharField(max_length=120, blank=None, null=True)
    number = models.CharField(max_length=35, blank=None, null=True)
    floor = models.CharField(max_length=35, blank=True, default='')
    room_number = models.CharField(max_length=4, blank=True, default='')
    is_physical = models.BooleanField(default=False)
    is_shipping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    class Meta:
        verbose_name = 'User Address'
        verbose_name_plural = 'User Addresses'
