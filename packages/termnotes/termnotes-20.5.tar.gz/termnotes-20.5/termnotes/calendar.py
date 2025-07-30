import json
import os
from rich.table import Table
from rich.console import Console

console = Console()

current_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(current_dir, 'data.json')

# Initialize list if file is empty
if os.stat(data_file_path).st_size == 0:
  calendar_items = {}
else:
  with open(data_file_path, 'r') as f:
    calendar_items = json.load(f)

def open_calendar():
  table = Table(title="Calendar")
  table.add_column("Date", justify="left", style="gray", no_wrap=True)
  table.add_column("Note", justify="left", style="aquamarine1")

  if calendar_items:
    for name, date in calendar_items.items():
      table.add_row(date, name)
  else:
    table.add_row("...", "...")

  console.print(table)
