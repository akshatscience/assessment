from django.db import models



class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, default="India")

    def __str__(self):
        return f"{self.name}, {self.country}"

class WeatherRecord(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="weather_records")
    temperature = models.FloatField(help_text="Temperature in Celsius")
    humidity = models.FloatField()
    condition = models.CharField(max_length=200)
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city.name}  {self.temperature}°C ({self.condition})"
