from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from applications.models import Application
from tenants.models import Tenant, TenantLog
from engines.models import DatabaseServer
from tenants.utils import credentials_generator, TenantManager

from django.utils.translation import ugettext_lazy as _


@receiver(post_save, sender=Application)
def tenant_creation_handler(sender, instance, created, **kwargs):
    if created:

        server = None
        uid = instance.uid
        try:
            server = DatabaseServer.objects.get(id=1)
        except DatabaseServer.DoesNotExist:
            print('DatabaseServer objects DoesNotExist')

        # Create and store tenant definition
        if not server:
            raise Exception('Server must be defined for tenant creation')

        db_name = ''.join([chr for chr in str(uid).replace('-', '') if chr.isalpha()])
        db_user = credentials_generator()
        db_password = credentials_generator()
        alias = db_name
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
            message=_('Tenant object created for app {uid}'.format(uid=instance.uid))
        )

        #Create database and sql Credentials
        tenant_manager = TenantManager(tenant)
        tenant_manager.create_database()
        tenant_manager.create_db_user()
        tenant_manager.grant_privileges()
        tenant_manager.sync_database()


@receiver(post_delete, sender=Tenant)
def tenant_remove_handler(sender, instance, using, **kwargs):
    tenant_manager = TenantManager(instance)
    tenant_manager.drop_db_user()
    tenant_manager.drop_database()
