from django.urls import reverse
from rest_framework.test import APITestCase

from apps.users.tests.factories import StaffFactory


class LanguageTestAPI(APITestCase):

    def test_language(self):
        staff = StaffFactory(is_staff=True, is_superuser=True)

        url = reverse('change-language')
        self.client.force_authenticate(user=staff)
        response = self.client.post(url, data={'language': 'en'})
        self.assertEqual(response.status_code, 200, response.data)

        staff.refresh_from_db()
        self.assertEqual(staff.language, 'en', response.data)
