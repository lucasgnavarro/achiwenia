import random
from django.conf import settings
from .models import Tenant, TenantLog
from psycopg2 import connect
from psycopg2._psycopg import IntegrityError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django.utils.translation import ugettext_lazy as _


def credentials_generator(length=8):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    pw_length = int(length)
    mypw = ''

    for i in range(pw_length):
        next_index = random.randrange(26)
        mypw += alphabet[next_index]

    return mypw


class TenantManager:

    def __init__(self):
        self.db_attrs = settings.DATABASES['default']

    def create_database(self, tenant: Tenant):
        try:
            con = connect(
                host=self.db_attrs['HOST'],
                dbname=tenant.db_server.host,
                user=self.db_attrs['USER'],
                password=self.db_attrs['PASSWORD']
            )
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = con.cursor()
            cur.execute('CREATE DATABASE ' + tenant.db_name)
            cur.close()
            con.close()

            TenantLog.objects.create(
                tenant=tenant,
                message=_(
                    'Database {uid} for tenant id={tenant_id} was created'.format(
                        uid=tenant.alias, tenant_id=tenant.id
                    )
                )
            )

            # synchronized = False
            # if sync_db:
            #     sync_schema(db_alias=schema_name)
            #     synchronized = True
            #
            # return {'_error': False, '_message': '', 'synchronized': synchronized}
        except IntegrityError:

            TenantLog.objects.create(
                tenant=tenant,
                message=_(
                    'Error on create database {uid} for tenant id={tenant_id}'.format(
                        uid=tenant.alias, tenant_id=tenant.id, log_level='E'
                    )
                )
            )

    def create_db_user(self): #TODO
        pass

    def create_db_password(self): #TODO
        pass

    def check_schema_sync(self): #TODO
        pass

    def sync_database(self): #TODO
        pass
