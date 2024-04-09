from apps.users.tests.factories import PlayerFactory
from django.urls import reverse
from rest_framework.test import APITestCase


class SchemeTestAPI(APITestCase):

    def test_scheme_api(self):
        player = PlayerFactory(is_staff=True, is_superuser=True)

        url = reverse('get-sections')
        self.client.force_authenticate(user=player)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.data)
