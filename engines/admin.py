from django.contrib import admin
from .models import DatabaseServer


class DatabaseServerAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


# Register your models here.
admin.site.register(DatabaseServer, DatabaseServerAdmin)
