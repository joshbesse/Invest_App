from pathlib import Path
import json
from datetime import date
import os

def get_today_ticker_group(json_path="../data/ticker_groups.json", manual_index=None):
    # create Path to ticker groups file
    groups_path = Path(json_path)

    if not groups_path.exists():
        print("Ticker groups file not found.")
        return []
    
    # read ticker groups from json file
    with open(groups_path, "r") as f:
        groups = json.load(f)

    if not groups:
        print("Ticker groups file is empty.")
        return []

    # set index as manual input if exists otherwise calculate based on date
    if manual_index:
        group_index = manual_index
    else:
        group_index = date.today().toordinal() % len(groups)
    
    # return group with set index
    return groups[group_index]