from django.contrib import admin
from .models import UserProfile, UserAddress
from applications.models import ApplicationByUser


class UserAddressInline(admin.TabularInline):
    model = UserAddress


class ApplicationByUserInline(admin.TabularInline):
    model = ApplicationByUser


class UserProfileAdmin(admin.ModelAdmin):
    inlines = [UserAddressInline, ApplicationByUserInline]


admin.site.register(UserProfile, UserProfileAdmin)
