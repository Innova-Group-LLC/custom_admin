import datetime

from django.contrib.auth import get_user_model
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase

from custom_admin.api.tests.urls import ADMIN_URLS
from custom_admin.models.admin_log import AdminLog, AdminLogType

User = get_user_model()

ATTRS = '?page=1&limit=25&filter_info=%257B%2522search%2522%253A%2522usern%2522%252C%2522filters%2522%253A%257B%2522section%2522%253A%2522note%2522%252C%2522staff%2522%253A%255B2%255D%252C%2522action_type%2522%253A%2522create%2522%252C%2522created_at%2522%253A%257B%2522from%2522%253A%25222024-05-08T01%253A48%253A00%2522%252C%2522to%2522%253A%25222024-05-23T01%253A48%253A00%2522%257D%257D%257D'


@override_settings(ADMIN_URLS=ADMIN_URLS)
class FiltersTestAPI(APITestCase):

    def setUp(self) -> None:
        self.admin = User.objects.create(
            id=2,
            username="username",
            is_staff=True,
            is_superuser=True,
        )
        self.other_admin = User.objects.create(
            id=3,
            username="other",
            is_staff=True,
            is_superuser=True,
        )

        AdminLog.objects.create(
            staff=self.admin,
            section='note',
            action_type=AdminLogType.CREATE,
            created_at=datetime.datetime(2024, 5, 10),
        )
        AdminLog.objects.create(
            staff=self.admin,
            section='note',
            action_type=AdminLogType.CREATE,
            created_at=datetime.datetime(2021, 5, 5),
        )
        AdminLog.objects.create(
            staff=self.other_admin,
            section='note',
            action_type=AdminLogType.CREATE,
            created_at=datetime.datetime(2021, 11, 16),
        )
        AdminLog.objects.create(
            staff=self.other_admin,
            section='section',
            action_type=AdminLogType.ACTION,
            created_at=datetime.datetime(2021, 11, 16),
        )

    def test_api_filter(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('adminlog-list')
        response = self.client.get(f'{url}?{ATTRS}')
        self.assertEqual(response.status_code, 200, response.content.decode())

        data = response.json()
        self.assertEqual(data['count'], 1)
