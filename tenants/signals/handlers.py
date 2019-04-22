from django.db.models.signals import post_save
from django.dispatch import receiver
from applications.models import Application
from tenants.models import Tenant, TenantLog
from engines.models import DatabaseServer
from tenants.utils import credentials_generator

from django.utils.translation import ugettext_lazy as _


@receiver(post_save, sender=Application)
def tenant_creation_handler(sender, instance, created, **kwargs):
    if created:
        print(instance.uid)
        print('CREAME EL TENANT')
        print(kwargs)
        server = None
        uid = instance.uid
        try:
            server = DatabaseServer.objects.get(id=1)
        except DatabaseServer.DoesNotExist:
            print('DatabaseServer objects DoesNotExist')

        # Create and store tenant definition
        if server:
            db_name = uid
            db_user = credentials_generator()
            db_password = credentials_generator()
            alias = uid
            tenant = Tenant(
                application=instance,
                db_server=server,
                db_name=db_name,
                db_user=db_user,
                db_password=db_password,
                alias=alias
            )
            tenant.save()

            TenantLog.objects.create(
                tenant=tenant,
                message=_('Tenant object was created')
            )

