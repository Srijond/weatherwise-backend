import json
import requests
from datetime import datetime, timedelta


def handle(*args, **kwargs):
        from weather_advisor.models import TemperatureForecast
        # Load district data from JSON file
        with open('/Users/srijon/Desktop/Personal/AB Project/weatherwise-backend/weather_advisor/district_info.json', 'r') as f:
            district_data = json.load(f)
        
        today = datetime.now()

        for district in district_data.get('districts'):
            name = district['name']
            lat = district['lat']
            lon = district['long']
            district_id = district['id']
           

            # Make a single API call to get the 7-day forecast
            response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}8&hourly=temperature_2m&forecast_days=7')
            data = response.json()

            # Extract temperatures at 2 PM (14:00) for the next 7 days
            hourly_times = data['hourly']['time']
            hourly_temps = data['hourly']['temperature_2m']
            print('hello')
            
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
                        date=date,
                        defaults={'temperature_at_2pm': temperature_at_2pm}
                    )




