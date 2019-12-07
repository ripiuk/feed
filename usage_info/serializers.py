import typing as typ

from rest_framework import serializers

from .models import UsageInfo


class CPIFieldModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(CPIFieldModelSerializer, self).__init__(*args, **kwargs)
        cpi = self.context['request'].query_params.get('cpi') if self.context else None
        if not cpi or (cpi and cpi != '1'):
            self.fields.pop('cpi')


class UsageInfoSerializer(CPIFieldModelSerializer, serializers.HyperlinkedModelSerializer):
    date = serializers.SerializerMethodField(required=False, allow_null=True)
    channel = serializers.SerializerMethodField(required=False, allow_null=True)
    country = serializers.SerializerMethodField(required=False, allow_null=True)
    os = serializers.SerializerMethodField(required=False, allow_null=True)
    cpi = serializers.SerializerMethodField(required=False, allow_null=True)

    class Meta:
        model = UsageInfo
        fields = (
            'date', 'channel', 'country', 'os', 'impressions',
            'clicks', 'installs', 'spend', 'revenue', 'cpi',
        )

    @staticmethod
    def _get_from_model(obj: typ.Union[dict, UsageInfo], field: str) -> typ.Any:
        return getattr(obj, field) if hasattr(obj, field) else \
            obj.get(field) if isinstance(obj, dict) else None

    def get_date(self, obj: typ.Union[dict, UsageInfo]) -> typ.Any:
        return self._get_from_model(obj, 'date')

    def get_channel(self, obj: typ.Union[dict, UsageInfo]) -> typ.Any:
        return self._get_from_model(obj, 'channel')

    def get_country(self, obj: typ.Union[dict, UsageInfo]) -> typ.Any:
        return self._get_from_model(obj, 'country')

    def get_os(self, obj: typ.Union[dict, UsageInfo]) -> typ.Any:
        return self._get_from_model(obj, 'os')

    def get_cpi(self, obj: typ.Union[dict, UsageInfo]) -> typ.Optional[float]:
        spend = self._get_from_model(obj, 'spend')
        installs = self._get_from_model(obj, 'installs')
        if spend and installs:
            return spend / installs
        return None
