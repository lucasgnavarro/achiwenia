from django.db import models
from applications.models import Application
from engines.models import DatabaseServer


class Tenant(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, null=False, blank=False,)
    db_server = models.ForeignKey(DatabaseServer, on_delete=models.PROTECT, null=False, blank=False)
    db_name = models.CharField(max_length=255, default='', null=False, blank=False)
    db_user = models.CharField(max_length=255, default='', null=False, blank=False)
    db_password = models.CharField(max_length=255, default='', null=False, blank=False)
    options = models.CharField(max_length=255, default='', null=False, blank=False)
    alias = models.CharField(max_length=255, default='', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # db_engine = models.CharField(max_length=255, default='', null=False, blank=False)
    # host = models.CharField(max_length=255, default='', null=False, blank=False)
    # port = models.CharField(max_length=255, default='', null=False, blank=False)


class TenantLog(models.Model):
    LOG_LEVELS = (
        ('I', 'INFO'),
        ('W', 'WARN'),
        ('E', 'ERROR')
    )
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, null=False, blank=False
    )
    message = models.CharField(max_length=255, blank=False, null=False)
    log_level = models.CharField(max_length=1, choices=LOG_LEVELS, default='I')
    date = models.DateTimeField(auto_now_add=True)
