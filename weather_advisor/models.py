from django.db import models

# Create your models here.



class TemperatureForecast(models.Model):
    district_id = models.IntegerField()
    date = models.DateField()
    temperature_at_2pm = models.FloatField()

    def __str__(self):
        return f"{self.district.name} - {self.date}: {self.temperature_at_2pm}°C"

