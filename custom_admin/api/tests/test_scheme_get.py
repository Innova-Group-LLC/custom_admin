from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class SchemeTestAPI(APITestCase):
    urls = 'custom_admin.api.tests.urls'

    def test_scheme_api(self):
        user = User.objects.create(username="username", is_staff=True)
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse('get-sections'))
        self.assertEqual(response.status_code, 200, response.content.decode())
