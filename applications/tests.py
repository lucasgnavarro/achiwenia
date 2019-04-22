from django.test import TestCase
from django.core.management import call_command

from django.contrib.auth.models import User
from .models import (
    Application, ApplicationUrl, ApplicationConfig, ApplicationByUser
)
from useraccounts.models import UserProfile

# Models Tests
class ApplicationTestCase(TestCase):

    def setUp(self) -> None:
        self.app = Application.objects.create(title='Tienda virtual', description='Application description Test')
        call_command('initdb')  # Custom Command
        self.user = User.objects.get(username='admin')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            tax_identification_number='20302161945'
        )

    def test_application_creation(self):
        test_app = Application.objects.get(title='Tienda virtual')
        self.assertEqual(test_app.description, 'Application description Test')

    def test_application_config(self):
        app_config = ApplicationConfig.objects.create(application=self.app)
        self.assertEqual(app_config.application.description, 'Application description Test')

    def test_application_url(self):
        urls = ('http://www.nianchuk.com', 'http://oztol.com', '192.168.0.5', '201.111.54.89')

        for url in urls:
            app_url = ApplicationUrl.objects.create(url=url, application=self.app)
            self.assertEqual(app_url.application.description, 'Application description Test')

    def test_app_by_user(self):
        app_by_user = ApplicationByUser.objects.create(
            application=self.app,
            user_profile=self.user_profile,
            is_staff=False,
            enabled=False
        )
        self.assertEqual(app_by_user.application.title, 'Tienda virtual')
        self.assertEqual(app_by_user.user_profile.user.username, 'admin')

