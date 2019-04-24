from django.contrib import admin
from .models import Tenant, TenantLog
# Register your models here.


class TenantLogsInline(admin.StackedInline):
    model = TenantLog
    fields = ('message', )

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class TenantAdmin(admin.ModelAdmin):

    inlines = (TenantLogsInline, )

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Tenant, TenantAdmin)
