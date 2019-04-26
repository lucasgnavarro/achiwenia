import random
from django.db import connections
from django.conf import settings
from django.core.management import call_command
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
        self.open_engine_connection()

    def open_engine_connection(self):
        """
        Open psycopg2 connection
        """
        if not self.con:
            self.con = connect(
                host=self.tenant.db_server.host,
                dbname=self.db_attrs['NAME'],
                user=self.db_attrs['USER'],
                password=self.db_attrs['PASSWORD']
            )
            self.con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    def close_engine_connection(self):
        """
        Close psycopg2 connection
        """
        self.con.close()

    def get_cursor(self):
        """
        :return: pgcursor for execute Queries
        """
        return self.con.cursor()

    def close_cursor(self, cursor):
        """
        Close PgCursor
        :param cursor:pgcursor to close
        """
        cursor.close()

    def exec_query(self, query=None):
        """
        Exec Sql query in current pgcursor
        :param query: Query to execute in current pgcursor
        :return:
        """
        try:
            cur = self.get_cursor()
            cur.execute(query)
            self.close_cursor(cur)

        except IntegrityError:

            TenantLog.objects.create(
                log_level='E',
                tenant=self.tenant,
                message=_(
                    'Error on exec_query {query} for app {{app}}'.format(
                        query=query, app=self.tenant.application.uid
                    )
                )
            )

    def create_database(self):
        """
        Execute query to create database in Pg Server
        """
        q = "create database {db_name};".format(db_name=self.tenant.db_name)
        self.exec_query(q)
        TenantLog.objects.create(
            tenant=self.tenant,
            message=_(
                'Database Creation for ({uid}) '.format(
                    uid=self.tenant.application.uid, tenant_id=self.tenant.id
                )
            )
        )

    def drop_database(self):
        """
        Call to exec_query to drop database in Pg Server
        """
        q = "DROP DATABASE [IF EXISTS] {db_name};".format(db_name=self.tenant.db_name)
        self.exec_query(q)

    def create_db_user(self):
        q = "CREATE USER {user} LOGIN PASSWORD '{password}';".format(
            user=self.tenant.db_user,
            password=self.tenant.db_password
        )
        self.exec_query(q)

        TenantLog.objects.create(
            tenant=self.tenant,
            message=_(
                'Pg Credentials creation for ({uid}) '.format(
                    uid=self.tenant.application.uid, tenant_id=self.tenant.id
                )
            )
        )

    def drop_db_user(self):
        """
        Call to exec_query to drop user in Pg Server
        """
        q = "DROP USER [IF EXISTS] {user};".format(
            user=self.tenant.db_user
        )
        self.exec_query(q)

    def grant_privileges(self):
        q = 'grant all privileges on database {dbname} to {user} ;'.format(
            dbname=self.tenant.db_name, user=self.tenant.db_user
        )
        self.exec_query(q)
        TenantLog.objects.create(
            tenant=self.tenant,
            message=_(
                'Pg Credentials/access established for ({uid}) '.format(
                    uid=self.tenant.application.uid, tenant_id=self.tenant.id
                )
            )
        )

    def run_db_tasks(self):
        self.create_database()
        self.create_db_user()
        self.grant_privileges()
        self.sync_database()

    @property
    def db_is_mapped(self) -> bool:
        """
        Check if the database is mapped in Django ORM connections
        :return: True if database is in connections.database else False
        """
        if self.tenant.alias in connections.databases:
            is_mapped = True
        else:
            try:
                connections.databases[self.tenant.alias] = {
                    'ENGINE': self.tenant.db_server.engine,
                    'NAME': self.tenant.db_name,
                    'USER': self.tenant.db_user,
                    'PASSWORD': self.tenant.db_password,
                    'HOST': self.tenant.db_server.host,
                    'PORT': self.tenant.db_server.port,
                }
                is_mapped = True

            except Exception as e: # Fixme Too broad exception clause
                is_mapped = False

        return is_mapped

    def sync_database(self):
        if self.db_is_mapped:
            call_command('migrate', database=self.tenant.alias)



