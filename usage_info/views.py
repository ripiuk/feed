from rest_framework import generics

from .serializers import UsageInfoSerializer
from .models import UsageInfo


class UsageInfoAll(generics.ListAPIView):
    queryset = UsageInfo.objects.all()
    serializer_class = UsageInfoSerializer
