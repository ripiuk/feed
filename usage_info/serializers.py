from rest_framework import serializers

from .models import UsageInfo


class UsageInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UsageInfo
        fields = (
            'date', 'channel', 'country', 'os', 'impressions',
            'clicks', 'installs', 'spend', 'revenue'
        )
