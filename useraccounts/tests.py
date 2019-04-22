# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from useraccounts.models import UserProfile, UserAddress


#   Models Tests
class UserTestCase(TestCase):
    def setUp(self) -> None:
        call_command('initdb')  # Custom Command
        self.user = User.objects.get(username='admin')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            tax_identification_number='20302161945'
        )

    def test_user_profile(self):
        self.assertEqual(self.user_profile.user.username, 'admin')
        self.assertEqual(self.user_profile.tax_identification_number, '20302161945')

    def test_user_address(self):
        address_list = [
            {'street': 'Avenida Colón', 'number': '4732'},
            {'street': 'Avenida Luro', 'number': '8542'}
        ]

        for address in address_list:
            UserAddress.objects.create(
                user_profile=self.user_profile,
                street=address['street'],
                number=address['number']
            )

        addr_obj = UserAddress.objects.get(id=1)

        self.assertEqual(addr_obj.user_profile.user.username, self.user_profile.user.username)
