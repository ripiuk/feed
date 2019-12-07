from django.urls import reverse
from django.db.models import Sum
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


class GetUsageInfoFilterChannels(BaseViewTest):

    def test_get_usage_info_by_one_channel(self):
        channel = "facebook"
        response = self.client.get(
            reverse("usage-info"), {"channels": channel}
        )
        expected = UsageInfo.objects.filter(channel__in=[channel])
        serialized = UsageInfoSerializer(expected, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serialized.data)

    def test_get_usage_info_many_channels(self):
        channels = "adcolony,facebook"
        response = self.client.get(
            reverse("usage-info"), {"channels": channels}
        )
        expected = UsageInfo.objects.filter(channel__in=channels.split(','))
        serialized = UsageInfoSerializer(expected, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serialized.data)

    def test_get_usage_info_empty_channel(self):
        channels = "adcolony,"
        response = self.client.get(
            reverse("usage-info"), {"channels": channels}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_usage_info_channel_as_digit(self):
        channels = "adcolony,12"
        response = self.client.get(
            reverse("usage-info"), {"channels": channels}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetUsageInfoFilterCountries(BaseViewTest):

    def test_get_usage_info_by_one_country(self):
        country = "US"
        response = self.client.get(
            reverse("usage-info"), {"countries": country}
        )
        expected = UsageInfo.objects.filter(country__in=[country])
        serialized = UsageInfoSerializer(expected, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serialized.data)

    def test_get_usage_info_many_countries(self):
        countries = "US,FR"
        response = self.client.get(
            reverse("usage-info"), {"countries": countries}
        )
        expected = UsageInfo.objects.filter(country__in=countries.split(','))
        serialized = UsageInfoSerializer(expected, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serialized.data)

    def test_get_usage_info_empty_country(self):
        countries = "US,"
        response = self.client.get(
            reverse("usage-info"), {"countries": countries}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_usage_info_country_as_digit(self):
        countries = "US,12"
        response = self.client.get(
            reverse("usage-info"), {"countries": countries}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetUsageInfoFilterOS(BaseViewTest):

    def test_get_usage_info_by_one_os(self):
        os = "ios"
        response = self.client.get(
            reverse("usage-info"), {"os": os}
        )
        expected = UsageInfo.objects.filter(os__in=[os])
        serialized = UsageInfoSerializer(expected, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serialized.data)

    def test_get_usage_info_many_os(self):
        os = "ios,android"
        response = self.client.get(
            reverse("usage-info"), {"os": os}
        )
        expected = UsageInfo.objects.filter(os__in=os.split(','))
        serialized = UsageInfoSerializer(expected, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serialized.data)

    def test_get_usage_info_empty_os(self):
        os = "ios,"
        response = self.client.get(
            reverse("usage-info"), {"os": os}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_usage_info_os_as_digit(self):
        os = "ios,12"
        response = self.client.get(
            reverse("usage-info"), {"os": os}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UsageInfoGroupBy(BaseViewTest):

    def test_group_usage_info_by_one_field(self):
        group_by = 'date'
        response = self.client.get(
            reverse("usage-info"), {"group_by": group_by}
        )
        expected = UsageInfo.objects.values(group_by).annotate(
            impressions=Sum('impressions'),
            clicks=Sum('clicks'),
            installs=Sum('installs'),
            spend=Sum('spend'),
            revenue=Sum('revenue')
        )
        serialized = UsageInfoSerializer(expected, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serialized.data)

    def test_group_usage_info_by_many_fields(self):
        group_by = 'date,channel,os'
        response = self.client.get(
            reverse("usage-info"), {"group_by": group_by}
        )
        group_by = group_by.split(',')
        expected = UsageInfo.objects.values(*group_by).annotate(
            impressions=Sum('impressions'),
            clicks=Sum('clicks'),
            installs=Sum('installs'),
            spend=Sum('spend'),
            revenue=Sum('revenue')
        )
        serialized = UsageInfoSerializer(expected, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serialized.data)

    def test_group_usage_info_by_not_allowed_field(self):
        group_by = 'clicks'
        response = self.client.get(
            reverse("usage-info"), {"group_by": group_by}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_group_usage_info_by_not_existing_field(self):
        group_by = 'not existing field'
        response = self.client.get(
            reverse("usage-info"), {"group_by": group_by}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UsageInfoSortBy(BaseViewTest):

    def test_sort_usage_info_by_one_field_asc(self):
        sort_by = 'date'
        response = self.client.get(
            reverse("usage-info"), {"sort_by": sort_by}
        )
        expected = UsageInfo.objects.order_by(sort_by)
        serialized = UsageInfoSerializer(expected, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serialized.data)

    def test_sort_usage_info_by_one_field_desc(self):
        sort_by = '-date'
        response = self.client.get(
            reverse("usage-info"), {"sort_by": sort_by}
        )
        expected = UsageInfo.objects.order_by(sort_by)
        serialized = UsageInfoSerializer(expected, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serialized.data)

    def test_sort_usage_info_by_many_fields(self):
        sort_by = '-date,clicks'
        response = self.client.get(
            reverse("usage-info"), {"sort_by": sort_by}
        )
        expected = UsageInfo.objects.order_by(*sort_by.split(','))
        serialized = UsageInfoSerializer(expected, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serialized.data)

    def test_sort_usage_info_by_not_existing_field(self):
        sort_by = 'not existing field'
        response = self.client.get(
            reverse("usage-info"), {"sort_by": sort_by}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
