import trafaret as t
from django.db.models import Sum
from django.http import QueryDict
from rest_framework import generics
from django.db.models.query import QuerySet
from rest_framework.exceptions import ParseError

from .models import UsageInfo
from .serializers import UsageInfoSerializer
from .validator import ValidationError, date_validator, comma_separated_str


class UsageInfoView(generics.ListAPIView):
    """
    Available parameters:
        date_from - get records from the specified date. e.g 2017-06-01
        date_to - get records till the specified date. e.g 2017-08-12
        channels - filter records by chosen channels. e.g 'facebook' or several 'facebook,adcolony,...'
        countries - filter records by chosen countries. e.g 'US' or several 'US,CA,...'
        os - filter records by chosen operating system. e.g 'android' or several 'android,ios,...'
        group_by - group by one ore several fields. e.g. 'date' or 'channel,country,os,...'
    """
    queryset = UsageInfo.objects.all()
    serializer_class = UsageInfoSerializer

    @staticmethod
    def _validate_query_params(query_params: QueryDict) -> None:
        """
        Validate all the needed query_params from the request

        :param query_params: query params from the request
        :return: None
        :raise ParseError: if query parameter is not valid
        """
        group_by_allowed_fields = {'date', 'channel', 'country', 'os'}
        schema = t.Dict({
            t.Key('date_from', optional=True): date_validator,
            t.Key('date_to', optional=True): date_validator,
            t.Key('channels', optional=True): comma_separated_str(),
            t.Key('countries', optional=True): comma_separated_str(),
            t.Key('os', optional=True): comma_separated_str(),
            t.Key('group_by', optional=True): comma_separated_str(group_by_allowed_fields),
        }, allow_extra='*')

        try:
            schema.check(query_params)
        except (ValidationError, t.DataError) as err:
            raise ParseError(err)

    def get_queryset(self) -> QuerySet:
        self._validate_query_params(self.request.query_params)

        filter_params = {
            'date_from': lambda date: ('date__gte', date),
            'date_to': lambda date: ('date__lte', date),
            'channels': lambda chs: ('channel__in', map(str.strip, chs.split(','))),
            'countries': lambda ctr: ('country__in', map(str.strip, ctr.split(','))),
            'os': lambda os: ('os__in', map(str.strip, os.split(','))),
        }

        if self.request.query_params:
            if 'group_by' in self.request.query_params:
                group_by = map(str.strip, self.request.query_params['group_by'].split(','))
                self.queryset = UsageInfo.objects.values(*group_by).annotate(
                    impressions=Sum('impressions'),
                    clicks=Sum('clicks'),
                    installs=Sum('installs'),
                    spend=Sum('spend'),
                    revenue=Sum('revenue')
                )

            params_to_filter = (
                filter_params[param](val)
                for param, val in self.request.query_params.items()
                if param in filter_params
            )
            self.queryset = self.queryset.filter(**dict(params_to_filter))

        return self.queryset
