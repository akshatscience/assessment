from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
from .models import City, WeatherRecord
from .serializers import CitySerializer, WeatherRecordSerializer
import requests
import os


load_dotenv()

@api_view(["GET", "POST"])
def city_list(request):
    
    if request.method == "GET":
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def city_detail(request, pk):
    
    city = get_object_or_404(City, pk=pk)

    if request.method == "GET":
        serializer = CitySerializer(city)
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:
        partial = request.method == "PATCH"
        serializer = CitySerializer(city, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        city.delete()
        return Response({"message": "City deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def weatherrecord_list(request):
    
    if request.method == "GET":
        records = WeatherRecord.objects.select_related("city").order_by("-fetched_at")
        serializer = WeatherRecordSerializer(records, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = WeatherRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def weatherrecord_detail(request, pk):
    
    record = get_object_or_404(WeatherRecord, pk=pk)

    if request.method == "GET":
        serializer = WeatherRecordSerializer(record)
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:
        partial = request.method == "PATCH"
        serializer = WeatherRecordSerializer(record, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        record.delete()
        return Response({"message": "Record deleted"}, status=status.HTTP_204_NO_CONTENT)


# API integration
@api_view(["GET"])
def fetch_weather(request, city_id):
    
    #using api key fetch weather data of a particular city
    city = get_object_or_404(City, pk=city_id)
    api_key = os.getenv("API_KEY")
    print(api_key)
    if not api_key:
        return Response({"error": "Missing API_KEY"}, status=500)

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    print(data)
    if response.status_code != 200:
        return Response(
            {"error": "Failed to fetch data", "status": response.status_code},
            status=response.status_code,
        )

    
    record = WeatherRecord.objects.create(
        city=city,
        temperature=data["main"]["temp"],
        humidity=data["main"]["humidity"],
        condition=data["weather"][0]["description"],
    )

    return Response({
        "message": "Successfull",
        "city": city.name,
        "temperature": record.temperature,
        "condition": record.condition,
    })


