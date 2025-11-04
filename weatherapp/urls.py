from django.urls import path
from . import views
from . import report

urlpatterns = [
    
    path("data/cities/", views.city_list, name="city-list"),
    path("data/city/<int:pk>/", views.city_detail, name="city-detail"),

    path("data/weatherrecords/", views.weatherrecord_list, name="record-list"),
    path("data/weatherrecord/<int:pk>/", views.weatherrecord_detail, name="record-detail"),

    # Weather API Integration
    path("data/fetch/<int:city_id>/", views.fetch_weather, name="fetch-weather"),

    # Report URL
    path("report/", report.weather_report, name="weather-report"),
]