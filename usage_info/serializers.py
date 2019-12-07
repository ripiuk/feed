from rest_framework import serializers

from .models import UsageInfo


class UsageInfoSerializer(serializers.HyperlinkedModelSerializer):
    date = serializers.SerializerMethodField(required=False, allow_null=True)
    channel = serializers.SerializerMethodField(required=False, allow_null=True)
    country = serializers.SerializerMethodField(required=False, allow_null=True)
    os = serializers.SerializerMethodField(required=False, allow_null=True)

    class Meta:
        model = UsageInfo
        fields = (
            'date', 'channel', 'country', 'os', 'impressions',
            'clicks', 'installs', 'spend', 'revenue'
        )

    @staticmethod
    def get_date(obj):
        return obj.date if hasattr(obj, 'date') else \
            obj.get('date') if isinstance(obj, dict) else None

    @staticmethod
    def get_channel(obj):
        return obj.channel if hasattr(obj, 'channel') else \
            obj.get('channel') if isinstance(obj, dict) else None

    @staticmethod
    def get_country(obj):
        return obj.country if hasattr(obj, 'country') else \
            obj.get('country') if isinstance(obj, dict) else None

    @staticmethod
    def get_os(obj):
        return obj.os if hasattr(obj, 'os') else \
            obj.get('os') if isinstance(obj, dict) else None
