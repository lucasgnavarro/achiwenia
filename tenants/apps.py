from django.apps import AppConfig


class TenantsConfig(AppConfig):
    name = 'tenants'
    verbose_name = 'Tenant Configuration'

    def ready(self):
        from tenants.signals import handlers
