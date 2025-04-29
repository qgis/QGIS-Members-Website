import json
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Fetches GDP data from World Bank API and saves formatted JSON'

    def handle(self, *args, **options):
        api_url = f"https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?date={settings.GDP_YEAR}&format=json&per_page=300"
        output_file = os.path.join(settings.BASE_DIR, 'base_static', 'json', f'worldbank_gdp.json')
        
        self.stdout.write(self.style.SUCCESS('Fetching data from World Bank API...'))
        
        try:
            # Fetch data from API
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            
            # The actual data is in the second element of the response array
            raw_data = data[1]
            
            # Process and format the data
            formatted_data = {}
            for item in raw_data:
                if item['value'] is not None:  # Only include entries with GDP values
                    country_code = item['country']['id']
                    formatted_data[country_code] = item['value']
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Save formatted data
            with open(output_file, 'w') as f:
                json.dump(formatted_data, f, indent=2)
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully saved formatted data to {output_file}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Processed {len(formatted_data)} countries/regions')
            )
            
        except requests.exceptions.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Error fetching data from World Bank API: {str(e)}')
            )
        except (IndexError, KeyError) as e:
            self.stdout.write(
                self.style.ERROR(f'Error processing API response: {str(e)}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'An unexpected error occurred: {str(e)}')
            )