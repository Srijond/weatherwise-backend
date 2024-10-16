# weather/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
from django.db.models import Avg
from datetime import date, timedelta
from .models import TemperatureForecast
from .utils import  parse_date

def coolest_districts_view(request):
    

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

def compare_temperatures(request):
    if request.method == 'GET':
        # Get parameters from the request
        friend_location = request.GET.get('friend_location')  # Example: 'district1'
        destination = request.GET.get('destination')          # Example: 'district2'
        travel_date = request.GET.get('date')                 # Format: 'YYYY-MM-DD'

        
        friend_temp = None
        destination_temp = None

        if not all([friend_location, destination, travel_date]):
            return JsonResponse({'error': 'Please provide friend_location, destination, and date.'}, status=400)

        # Parse the travel date
        travel_date = parse_date(travel_date)
        if travel_date is None:
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)
        
        # Get temperature forecasts for both locations at 2 PM on the travel date
        try:
            friend_temp = TemperatureForecast.objects.get(district_name=friend_location, date=travel_date)
        except TemperatureForecast.DoesNotExist:
            # Fetch temperature from the API if not found in the database
            
            friend_temp_error = f'Temperature data not available for {friend_location} on {travel_date}.'

        try:
            destination_temp = TemperatureForecast.objects.get(district_name=destination, date=travel_date)
        except TemperatureForecast.DoesNotExist:
            destination_temp_error = f'Temperature data not available for {destination} on {travel_date}.'

           
        if friend_temp is None and destination_temp is None:
            return JsonResponse({
                'error': friend_temp_error + " " + destination_temp_error
            }, status=404)
        
        if friend_temp is None:
            return JsonResponse({'error': friend_temp_error}, status=404)

        if destination_temp is None:
            return JsonResponse({'error': destination_temp_error}, status=404)



        # Compare temperatures
        if friend_temp.temperature_at_2pm > destination_temp.temperature_at_2pm:
            decision = f"You should travel to {destination}."
        elif friend_temp.temperature_at_2pm < destination_temp.temperature_at_2pm:
            decision = f"You should stay at {friend_location}."
        else:
            decision = f"The temperatures are the same at both locations."

        response_data = {
            'friend_location': friend_location,
            'destination': destination,
            'travel_date': travel_date,
            'friend_temp': friend_temp.temperature_at_2pm,
            'destination_temp': friend_temp.temperature_at_2pm,
            'decision': decision
        }
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request method. Use GET.'}, status=405)
