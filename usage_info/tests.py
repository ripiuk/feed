from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient

from .models import UsageInfo
from .serializers import UsageInfoSerializer


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_usage_info(**kwargs):
        UsageInfo.objects.create(**kwargs)

    def setUp(self):
        self.create_usage_info(
            date='2019-12-06',
            channel='adcolony',
            country='US',
            os='Windows Mobile?',
            impressions='19887',
            clicks='494',
            installs='76',
            spend='148.2',
            revenue='149.04')

        self.create_usage_info(
            date='2018-11-12',
            channel='chartboost',
            country='CA',
            os='ios',
            impressions='1244',
            clicks='12',
            installs='4',
            spend='21.8',
            revenue='26.01')

        self.create_usage_info(
            date='2019-10-12',
            channel='facebook',
            country='FR',
            os='android',
            impressions='3350',
            clicks='69',
            installs='8',
            spend='34.5',
            revenue='0.0')


class GetAllUsageInfo(BaseViewTest):

    def test_get_all_usage_info(self):
        """
        Ensures that all usage info added in the setUp method
        exist when we make a GET request to the usage_info/ endpoint
        """
        response = self.client.get(
            reverse("usage-info")
        )
        expected = UsageInfo.objects.all()
        serialized = UsageInfoSerializer(expected, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serialized.data)


class GetUsageInfoFilterDate(BaseViewTest):

    def test_get_usage_info_from_date(self):
        date_from = "2018-11-13"
        response = self.client.get(
            reverse("usage-info"), {"date_from": date_from}
        )
        expected = UsageInfo.objects.filter(date__gte=date_from)
        serialized = UsageInfoSerializer(expected, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serialized.data)

    def test_get_usage_info_from_date_bad(self):
        date_from = "not valid date"
        response = self.client.get(
            reverse("usage-info"), {"date_from": date_from}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_usage_info_to_date(self):
        date_to = "2018-11-13"
        response = self.client.get(
            reverse("usage-info"), {"date_to": date_to}
        )
        expected = UsageInfo.objects.filter(date__lte=date_to)
        serialized = UsageInfoSerializer(expected, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serialized.data)

    def test_get_usage_info_to_date_bad(self):
        date_to = "2019-not valid"
        response = self.client.get(
            reverse("usage-info"), {"date_to": date_to}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_usage_info_from_date_with_to_date(self):
        date_from = "2017-07-10"
        date_to = "2018-11-13"
        response = self.client.get(
            reverse("usage-info"), {"date_from": date_from, "date_to": date_to}
        )
        expected = UsageInfo.objects.filter(
            date__gte=date_from).filter(date__lte=date_to)
        serialized = UsageInfoSerializer(expected, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serialized.data)
