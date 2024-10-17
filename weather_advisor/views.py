# weather/views.py
from django.shortcuts import render
from django.http import JsonResponse
import json
from django.core.cache import cache
from django.db.models import Avg
from datetime import date, timedelta
from .models import TemperatureForecast
from django.views.decorators.csrf import csrf_exempt
from .utils import  fetch_weather_temp, get_temperature, lat_long_by_name, parse_date

def coolest_districts(request):
    

    today = date.today()
    end_date = today + timedelta(days=7)

    # Query to calculate average temperature over the next 7 days
    averages = TemperatureForecast.objects.filter(
        date__range=(today, end_date)
    ).values('district_id','district_name').annotate(avg_temp=Avg('temperature_at_2pm')).order_by('avg_temp')[:10]

    if not averages.exists():
            return JsonResponse({'error': 'No temperature data available.'}, status=404)


    # Convert queryset to a list of dictionaries


    result = [{'district_name': avg['district_name'], 'avg_temp': avg['avg_temp']} for avg in averages]

    return JsonResponse(result, safe=False)

@csrf_exempt
def compare_temperatures(request):
    if request.method == 'POST':
        # Get parameters from the request
        try:
            body = json.loads(request.body)
            friend_location = body.get('friend_location')  # Example: 'district1'
            destination = body.get('destination')          # Example: 'district2'
            travel_date = body.get('date')                 # Format: 'YYYY-MM-DD'
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)


        

        if not all([friend_location, destination, travel_date]):
            return JsonResponse({'error': 'Please provide friend_location, destination, and date.'}, status=400)

        # Parse the travel date
        travel_date = parse_date(travel_date)
        if travel_date is None:
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)
        
        
         # Fetch temperatures for both locations
        friend_temp = get_temperature(friend_location, travel_date)
        destination_temp = get_temperature(destination, travel_date)
       

        if friend_temp is None or destination_temp is None:
            return JsonResponse({'error': 'Temperature data not available for one or both locations.'}, status=404)

        # Compare temperatures and decide
        if friend_temp > destination_temp:
            decision = f"You should travel to {destination}."
        elif friend_temp < destination_temp:
            decision = f"You should stay at {friend_location}."
        else:
            decision = f"The temperatures are the same at both locations."

        # Prepare response data
        response_data = {
            'friend_location': friend_location,
            'destination': destination,
            'travel_date': travel_date,
            'friend_temp': friend_temp,
            'destination_temp': destination_temp,
            'decision': decision
        }

        return JsonResponse(response_data)
    
    return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)

