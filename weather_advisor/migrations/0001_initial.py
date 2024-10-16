# Generated by Django 4.2.7 on 2024-10-16 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TemperatureForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district_id', models.IntegerField()),
                ('date', models.DateField()),
                ('temperature_at_2pm', models.FloatField()),
            ],
        ),
    ]
