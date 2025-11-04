from django.contrib import admin
from .models import City, WeatherRecord

# Register your models here.
admin.site.register(City)
admin.site.register(WeatherRecord)
