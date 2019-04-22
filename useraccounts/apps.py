from django.apps import AppConfig


class UseraccountsConfig(AppConfig):
    name = 'useraccounts'
    verbose_name = 'User Accounts'

    def ready(self):
        from useraccounts.signals import handlers
