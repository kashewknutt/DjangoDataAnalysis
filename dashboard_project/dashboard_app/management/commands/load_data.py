from datetime import datetime
from django.utils import timezone
import json
import os
from django.core.management.base import BaseCommand
from dashboard_app.models import DataEntry
from django.conf import settings

class Command(BaseCommand):
    help = 'Load data from JSON file into the database'

    def handle(self, *args, **kwargs):
        json_file_path = os.path.join(settings.BASE_DIR, 'dashboard_app', 'management', 'commands', 'json', 'jsondata.json')
        with open(json_file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                for entry in data:
                    added = self.parse_datetime(entry.get('added'))
                    published = self.parse_datetime(entry.get('published'))

                    # Handle empty strings for end_year and intensity
                    end_year = entry.get('end_year', None)
                    if end_year == '':
                        end_year = None

                    intensity = entry.get('intensity', None)
                    if intensity == '':
                        intensity = None

                    # Log and attempt to format invalid entries
                    if not all([added, published, entry.get('sector'), entry.get('topic'), entry.get('insight'),
                                entry.get('url'), entry.get('start_year'), entry.get('relevance'), entry.get('pestle'),
                                entry.get('source'), entry.get('title'), entry.get('likelihood')]):
                        self.stdout.write(self.style.WARNING(f"Invalid entry format or missing data: {entry}"))
                        continue

                    DataEntry.objects.create(
                        end_year=end_year,
                        intensity=intensity,
                        sector=entry['sector'],
                        topic=entry['topic'],
                        insight=entry['insight'],
                        url=entry['url'],
                        region=entry['region'],
                        start_year=entry['start_year'],
                        impact=entry['impact'],
                        added=added,
                        published=published,
                        country=entry['country'],
                        relevance=entry['relevance'],
                        pestle=entry['pestle'],
                        source=entry['source'],
                        title=entry['title'],
                        likelihood=entry['likelihood']
                    )
            except json.JSONDecodeError as e:
                self.stdout.write(self.style.ERROR(f"JSON decode error: {e}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))

    def parse_datetime(self, date_str):
        if date_str:
            try:
                naive_datetime = datetime.strptime(date_str, '%B, %d %Y %H:%M:%S')
                aware_datetime = timezone.make_aware(naive_datetime, timezone.get_current_timezone())
                return aware_datetime
            except ValueError as e:
                self.stdout.write(self.style.WARNING(f"Date conversion error: {e} for date: {date_str}"))
                return None
        return None
