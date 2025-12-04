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
    province_id = models.CharField(db_column='province_ID', primary_key=True, max_length=45)  # Field name made lowercase.
    province_name = models.CharField(db_column='province_name' ,max_length=45)

    class Meta:
        managed = False
        db_table = 'province'


class WeatherData(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    city_id = models.CharField(db_column='city_ID', max_length=45)  # Field name made lowercase.
    date = models.DateField(db_column='date')
    temperature = models.FloatField(db_column='temperature')
    precipitation = models.FloatField(db_column='precipitation')
    wind_speed = models.FloatField(db_column='wind_speed')
    wind_direction = models.CharField(db_column='wind_direction',max_length=45)
    air_pressure = models.FloatField(db_column='air_pressure')
    humidity = models.FloatField(db_column='humidity')
    cloud_cover = models.FloatField(db_column='cloud_cover')

    class Meta:
        managed = False
        db_table = 'weather_data'
