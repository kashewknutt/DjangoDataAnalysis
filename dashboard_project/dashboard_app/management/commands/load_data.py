import json
import os
from django.core.management.base import BaseCommand
from dashboard_app.models import DataEntry
from dashboard_project.dashboard_project import settings

class Command(BaseCommand):
    help = 'Load data from JSON file into the database'

    def handle(self, *args, **kwargs):
        json_file_path = os.path.join(settings.BASE_DIR, 'dashboard_app', 'management', 'commands', 'json', 'jsondata.json')
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            for entry in data:
                DataEntry.objects.create(
                    end_year=entry['end_year'],
                    intensity=entry['intensity'],
                    sector=entry['sector'],
                    topic=entry['topic'],
                    insight=entry['insight'],
                    url=entry['url'],
                    region=entry['region'],
                    start_year=entry['start_year'],
                    impact=entry['impact'],
                    added=entry['added'],
                    published=entry['published'],
                    country=entry['country'],
                    relevance=entry['relevance'],
                    pestle=entry['pestle'],
                    source=entry['source'],
                    title=entry['title'],
                    likelihood=entry['likelihood']
                )
