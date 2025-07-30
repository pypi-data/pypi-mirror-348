import json
import os
from rich.table import Table
from rich.console import Console
import importlib.resources

console = Console()

with importlib.resources.open_text('termnotes', 'data.json') as data_file:
  content = data_file.read()

if len(content.strip()) == 0:
  calendar_items = {}
else:
  calendar_items = json.loads(content)

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
