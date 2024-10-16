import json
import requests
from datetime import datetime, timedelta



def handle(*args, **kwargs):
        from weather_advisor.models import TemperatureForecast
        # Load district data from JSON file
        with open('weather_advisor/district_info.json', 'r') as f:
            district_data = json.load(f)
        
        today = datetime.now()
        for district in district_data.get('districts'):
            district_name = district['name']
            lat = district['lat']
            lon = district['long']
            district_id = district['id']
           

            # Make a single API call to get the 7-day forecast
            response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}8&hourly=temperature_2m&forecast_days=7')
            data = response.json()

            # Extract temperatures at 2 PM (14:00) for the next 7 days
            hourly_times = data['hourly']['time']
            hourly_temps = data['hourly']['temperature_2m']
            
            for i in range(7):  # Loop for the next 7 days
                date = (today + timedelta(days=i)).date()
                
                # Loop through the times and find the temperature at 2 PM (14:00) for the correct date
                temperature_at_2pm = None
                for j, time in enumerate(hourly_times):
                    if time.startswith(str(date)) and time.endswith('14:00'):
                        temperature_at_2pm = hourly_temps[j]
                        break

                if temperature_at_2pm is not None:
                    # Update or create the temperature forecast record
                    TemperatureForecast.objects.update_or_create(
                        district_id=district_id,
                        district_name=district_name,
                        date=date,
                        defaults={'temperature_at_2pm': temperature_at_2pm}
                    )




def parse_date(date_str):
    try:
        # Attempt to parse the date string in the format 'YYYY-MM-DD'
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        # If parsing fails, return None or raise an error
        return None

def lat_long_by_name(district_name):
    with open('weather_advisor/district_info.json', 'r') as f:
            district_data = json.load(f)
    for district in district_data.get('districts'):
        if district['name'].lower() == district_name.lower():  # Case insensitive comparison
            return {
                'lat': district['lat'],
                'long': district['long']
            }
    return None 




def fetch_weather_temp(lat, lon, travel_date):
    """Fetch the temperature at 2 PM for a given latitude, longitude, and date."""

    formatted_date = travel_date.strftime('%Y-%m-%d')
    formatted_date_time = f'{formatted_date}T14:00'
    response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&start_hour={formatted_date_time}&end_hour={formatted_date_time}')
    
    if response.status_code != 200:
        return None

    data = response.json()    
    # Extract the temperature at 2 PM for the specific date
    curr_temp = data.get('hourly').get('temperature_2m')[0]
    if curr_temp:
         return curr_temp
    return None

def get_temperature(district_name, date):
    from .models import TemperatureForecast
    try:
        temp_record = TemperatureForecast.objects.get(district_name=district_name, date=date)
        return temp_record.temperature_at_2pm
    except TemperatureForecast.DoesNotExist:
        lat_long = lat_long_by_name(district_name)
        if lat_long:
            return fetch_weather_temp(lat_long.get('lat'), lat_long.get('long'), date)
        return None