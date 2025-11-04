
import pandas as pd
from io import StringIO
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import WeatherRecord

@api_view(["GET"])
def weather_report(request):
   
    records = WeatherRecord.objects.select_related("city").values(
        "city__name", "temperature", "humidity", "fetched_at"
    )
    
    if not records.exists():
        return Response({"message": "No weather data available"}, status=404)

    df = pd.DataFrame.from_records(records)

    df.rename(columns={
        "city__name": "City",
        "temperature": "Temperature (°C)",
        "humidity": "Humidity (%)",
        "fetched_at": "Fetched At"
    }, inplace=True)


    summary = (
        df.groupby("City")
        .agg({
            "Temperature (°C)": ["mean", "min", "max"],
            "Humidity (%)": ["mean", "min", "max"]
        })
        .round(2)
    )
    summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
    summary.reset_index(inplace=True)

   
    output_format = request.GET.get("format", "json")

    if output_format == "csv":
        buffer = StringIO()
        summary.to_csv(buffer, index=False)
        response = HttpResponse(buffer.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="weather_report.csv"'
        return response

    
    return Response(summary.to_dict(orient="records"))
