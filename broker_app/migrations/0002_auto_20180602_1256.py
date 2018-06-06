# Generated by Django 2.0.4 on 2018-06-02 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('broker_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='landlordresponse',
            name='supplemental_garage_unreserved_parking_rates_USD_per_DAY',
        ),
        migrations.AddField(
            model_name='building',
            name='supplemental_garage_unreserved_parking_rates_USD_per_DAY',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]