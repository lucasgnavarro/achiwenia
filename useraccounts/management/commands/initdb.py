from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User


class Command(BaseCommand):

    help = 'Initialize database'

    def create_super_user(self):
        try:
            self.stdout.write(self.style.SQL_FIELD('------ Create default admin user ------'))
            User.objects.create_user(username='admin', password='admin', is_staff=True, is_superuser=True)
            self.stdout.write('\tUsername: admin, password: admin', ending=' ')
            self.stdout.write(self.style.SUCCESS('(OK)'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))

    def load_default_data(self):
        self.stdout.write(self.style.SQL_FIELD('------ Load default data ------'))
        self.stdout.write('\tLoad default user roles...', ending=' ')
        call_command('loaddata', 'useraccounts/fixtures/user-roles.json')
        self.stdout.write('\tUser roles...', ending=' ')
        self.stdout.write(self.style.SUCCESS('OK'))

        self.stdout.write('\tLoad default database engines...', ending=' ')
        call_command('loaddata', 'engines/fixtures/database-servers.json')
        self.stdout.write('\tUser roles...', ending=' ')
        self.stdout.write(self.style.SUCCESS('OK'))

    def handle(self, *args, **options):
        self.create_super_user()
        self.load_default_data()

