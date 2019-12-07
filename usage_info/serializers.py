import typing as typ

from rest_framework import serializers

from .models import UsageInfo


class UsageInfoSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.SerializerMethodField(required=False, allow_null=True)
    channel = serializers.SerializerMethodField(required=False, allow_null=True)
    country = serializers.SerializerMethodField(required=False, allow_null=True)
    os = serializers.SerializerMethodField(required=False, allow_null=True)
    cpi = serializers.FloatField(required=False)

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
