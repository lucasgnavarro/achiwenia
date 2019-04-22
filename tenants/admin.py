from django.contrib import admin
from .models import Tenant
# Register your models here.


# class TenantAdmin(admin.ModelAdmin):
#
#     def has_change_permission(self, request, obj=None):
#         return False
#
#     def has_delete_permission(self, request, obj=None):
#         print(self.__dict__)
#         return True
#     #     return False

admin.site.register(Tenant)
