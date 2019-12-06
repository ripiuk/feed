# Generated by Django 3.0 on 2019-12-06 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsageInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('channel', models.CharField(max_length=256)),
                ('country', models.CharField(max_length=3)),
                ('os', models.CharField(max_length=60)),
                ('impressions', models.PositiveIntegerField()),
                ('clicks', models.PositiveIntegerField()),
                ('installs', models.PositiveIntegerField()),
                ('spend', models.FloatField()),
                ('revenue', models.FloatField()),
            ],
        ),
    ]