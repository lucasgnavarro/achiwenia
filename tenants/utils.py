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

    def __init__(self, tenant: Tenant):
        self.db_attrs = settings.DATABASES['default']
        self.tenant = tenant
        self.con = None

        # Init engine connection
        self.set_engine_connection()

    def set_engine_connection(self):
        if not self.con:
            self.con = connect(
                host=self.tenant.db_server.host,
                dbname=self.db_attrs['NAME'],
                user=self.db_attrs['USER'],
                password=self.db_attrs['PASSWORD']
            )
            self.con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    def close_engine_connection(self):
        self.con.close()

    def get_cursor(self):
        return self.con.cursor()

    def close_cursor(self, cursor):
        cursor.close()

    def exec_command(self, query=None):
        try:
            cur = self.get_cursor()
            cur.execute(query)
            self.close_cursor(cur)

        except IntegrityError:

            TenantLog.objects.create(
                tenant=self.tenant,
                message=_(
                    'Error on exec_command {query} for tenant id={tenant_id}'.format(
                        query=query, tenant_id=self.tenant.id, log_level='E'
                    )
                )
            )

    def create_database(self):
            db_name = str(self.tenant.db_name).replace('-', '')
            q = "create database {db_name};".format(db_name=db_name)
          #  try:
            print(q)
            self.exec_command(q)
            TenantLog.objects.create(
                tenant=self.tenant,
                message=_(
                    'Database {uid} for tenant id={tenant_id} was created'.format(
                        uid=self.tenant.alias, tenant_id=self.tenant.id
                    )
                )
            )

                # synchronized = False
                # if sync_db:
                #     sync_schema(db_alias=schema_name)
                #     synchronized = True
                #
                # return {'_error': False, '_message': '', 'synchronized': synchronized}
            #except Exception as e:



    def create_db_user(self): #TODO
        pass

    def create_db_password(self): #TODO
        pass

    def check_schema_sync(self): #TODO
        pass

    def sync_database(self): #TODO
        pass
