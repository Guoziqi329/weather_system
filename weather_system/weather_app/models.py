from django.db import models


# Create your models here.

class City(models.Model):
    city_id = models.CharField(db_column='city_ID', primary_key=True, max_length=45)  # Field name made lowercase.
    city_name = models.CharField(max_length=45)
    province_id = models.CharField(db_column='province_ID', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'city'


class Province(models.Model):
    province_name = models.CharField(max_length=45)
    province_id = models.CharField(db_column='province_ID', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'province'


class WeatherData(models.Model):
    city_id = models.CharField(db_column='city_ID', max_length=45)  # Field name made lowercase.
    date = models.DateField()
    temperature = models.FloatField()
    precipitation = models.FloatField()
    wind_speed = models.FloatField()
    wind_direction = models.CharField(max_length=45)
    air_pressure = models.FloatField()
    humidity = models.FloatField()
    cloud_cover = models.FloatField()

    class Meta:
        managed = False
        db_table = 'weather_data'
