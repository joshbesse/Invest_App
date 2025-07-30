from django.core.management.base import BaseCommand
from invest.models import Stock
import random
import json
from pathlib import Path

class Command(BaseCommand):
    help = "Create rotating ticker groups and save to json"

    def handle(self, *args, **options):
        group_count = 5
        output_path = Path("invest/data/ticker_groups.json")

        # retrieve all tickers from Stock table
        tickers = list(Stock.objects.values_list("ticker", flat=True))

        if not tickers:
            print("No tickers found in Stock table.")
            return

        # shuffle tickers for randomized groupings
        random.shuffle(tickers)

        # slice tickers list to make groups
        groups = [tickers[i::group_count] for i in range(group_count)]

        # save ticker groups to json
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(groups, f, indent=2)

        print(f"Created {group_count} ticker groups ({len(tickers)} tickers) at {output_path}")    