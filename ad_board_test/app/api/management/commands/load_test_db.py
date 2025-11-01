import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load initial data from a JSON file.'

    def handle(self, *args, **kwargs):
        # Get path to 'test_data.json'
        json_file_path = os.path.join(
            settings.BASE_DIR, 'data', 'test_data.json'
        )

        # Check if the file exists
        if not os.path.exists(json_file_path):
            self.stderr.write(
                self.style.ERROR(f'File not found: {json_file_path}')
            )
            return

        # Call the command to load data from a JSON file
        call_command('loaddata', json_file_path)
