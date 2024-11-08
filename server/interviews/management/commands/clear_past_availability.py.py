from django.core.management.base import BaseCommand
from interviews.models import *
from datetime import date

class Command(BaseCommand):
    help = 'Clear all availability records that are in the past'

    def handle(self, *args, **kwargs):
        # Filter for past availabilities
        past_availabilities = Availability.objects.filter(available_date__lt=date.today())

        # Count the number of availabilities being deleted for logging
        count = past_availabilities.count()
        if count > 0:
            past_availabilities.delete()
            self.stdout.write(f'Successfully deleted {count} past availability records.')
        else:
            self.stdout.write('No past availability records to delete.')
