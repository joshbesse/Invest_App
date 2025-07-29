from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Collect and insert price data for Price table and calculate and insert indicators for Indicator table"