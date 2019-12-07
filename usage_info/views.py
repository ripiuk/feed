import trafaret as t
from django.http import QueryDict
from rest_framework import generics
from django.db.models.query import QuerySet
from rest_framework.exceptions import ParseError

from .models import UsageInfo
from .serializers import UsageInfoSerializer
from .validator import ValidationError, date_validator


class UsageInfoAll(generics.ListAPIView):
    """
    Available parameters:
        date_from - get records from the specified date. e.g 2017-06-01
        date_to - get records till the specified date. e.g 2017-08-12
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
        schema = t.Dict({
            t.Key('date_from', optional=True): date_validator,
            t.Key('date_to', optional=True): date_validator,
        }, allow_extra='*')

        try:
            schema.check(query_params)
        except (ValidationError, t.DataError) as err:
            raise ParseError(err)

    def get_queryset(self) -> QuerySet:
        self._validate_query_params(self.request.query_params)

        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        # TODO: Move queryset creation from here
        if date_from:
            self.queryset = self.queryset.filter(date__gte=date_from)
        if date_to:
            self.queryset = self.queryset.filter(date__lte=date_to)
        return self.queryset
