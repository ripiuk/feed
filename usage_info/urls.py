from django.urls import include, path

from .views import UsageInfoAll

urlpatterns = [
    path('', UsageInfoAll.as_view(), name='usage-info-all'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
