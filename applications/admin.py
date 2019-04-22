from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.forms.models import BaseInlineFormSet
from django.forms import TextInput

from .models import (
    Application, ApplicationConfig, ApplicationUrl,  ApplicationByUser
)
from tenants.models import Tenant

admin.site.site_header = _('Admin - Centralized Authentication Service')


class ApplicationConfigInline(admin.TabularInline):
    model = ApplicationConfig
    readonly_fields = ['login_bg_image']

    def login_bg_image(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.login_bg_img.url,
                width=300,
                height=300,
            )
        )


class ApplicationUrlInline(admin.TabularInline):
    model = ApplicationUrl


class ApplicationByUserInline(admin.TabularInline):
    model = ApplicationByUser


class ApplicationAdmin(admin.ModelAdmin):
    readonly_fields = ['uid']
    inlines = (
        ApplicationConfigInline,
        ApplicationUrlInline,
        ApplicationByUserInline,
    )


admin.site.register(Application, ApplicationAdmin)
