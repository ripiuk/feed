from django.urls import include, path

from .views import UsageInfoView

urlpatterns = [
    path('', UsageInfoView.as_view(), name='usage-info'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
