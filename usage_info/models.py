from django.db import models


class UsageInfo(models.Model):
    date = models.DateField(auto_now_add=True, blank=False)
    channel = models.CharField(max_length=256, blank=False)
    country = models.CharField(max_length=3, blank=False)
    os = models.CharField(max_length=60, blank=False)
    impressions = models.PositiveIntegerField(blank=False)
    clicks = models.PositiveIntegerField(blank=False)
    installs = models.PositiveIntegerField(blank=False)
    spend = models.FloatField(blank=False)
    revenue = models.FloatField(blank=False)

    def __str__(self):
        return f'{self.date} {self.channel} {self.os} {self.country}'
