import trafaret as t
from django.http import QueryDict
from rest_framework import generics
from rest_framework.exceptions import ParseError
from django.db.models import Sum, query, F, FloatField, ExpressionWrapper

from .models import UsageInfo
from .serializers import UsageInfoSerializer
from .validator import ValidationError, date_validator, comma_separated_str


class UsageInfoView(generics.ListAPIView):
    """
    Available url parameters:
        date_from - get records from the specified date. e.g 2017-06-01
        date_to - get records till the specified date. e.g 2017-08-12
        channels - filter records by chosen channels. e.g 'facebook' or several 'facebook,adcolony,...'
        countries - filter records by chosen countries. e.g 'US' or several 'US,CA,...'
        os - filter records by chosen operating system. e.g 'android' or several 'android,ios,...'
        group_by - group by one ore several fields. e.g. 'date' or 'channel,country,os,...'
        sort_by - group by one ore several fields. e.g. 'channel' or 'installs,-revenue,os,...' ('-' means descending)
        cpi - CPI metric (cost per install). You can include it by adding 'cpi=1'
    """
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
        sort_by_allowed_fields = {
            'date', 'channel', 'country', 'os', 'impressions',
            'clicks', 'installs', 'spend', 'revenue', 'cpi'}
        sort_by_allowed_fields = sort_by_allowed_fields | {f'-{field}' for field in sort_by_allowed_fields}

        schema = t.Dict({
            t.Key('date_from', optional=True): date_validator,
            t.Key('date_to', optional=True): date_validator,
            t.Key('channels', optional=True): comma_separated_str(),
            t.Key('countries', optional=True): comma_separated_str(),
            t.Key('os', optional=True): comma_separated_str(),
            t.Key('group_by', optional=True): comma_separated_str(group_by_allowed_fields),
            t.Key('sort_by', optional=True): comma_separated_str(sort_by_allowed_fields),
        }, allow_extra='*')

        try:
            schema.check(query_params)
        except (ValidationError, t.DataError) as err:
            raise ParseError(err)

    def get_queryset(self) -> query.QuerySet:
        queryset = UsageInfo.objects.all()

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
                queryset = UsageInfo.objects.values(*group_by).annotate(
                    impressions=Sum('impressions'),
                    clicks=Sum('clicks'),
                    installs=Sum('installs', output_field=FloatField()),
                    spend=Sum('spend', output_field=FloatField()),
                    revenue=Sum('revenue')
                )

            cpi = self.request.query_params.get('cpi')
            if cpi and cpi == '1':
                queryset = queryset.annotate(
                    cpi=ExpressionWrapper(
                        F('spend') / F('installs'),
                        output_field=FloatField()))

            if 'sort_by' in self.request.query_params:
                sort_by = list(map(str.strip, self.request.query_params['sort_by'].split(',')))
                if any(cpi_val in sort_by for cpi_val in ('cpi', '-cpi')) and cpi != '1':
                    raise ParseError('Can not sort by CPI. Please turn CPI on by adding cpi=1')
                queryset = queryset.order_by(*sort_by)

            params_to_filter = (
                filter_params[param](val)
                for param, val in self.request.query_params.items()
                if param in filter_params
            )
            queryset = queryset.filter(**dict(params_to_filter))

        return queryset
