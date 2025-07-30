import json
import os
from rich.table import Table
from rich.console import Console

console = Console()

def open_calendar():
  table = Table(title="Calendar")
  table.add_column("Date", justify="left", style="gray", no_wrap=True)
  table.add_column("Note", justify="left", style="aquamarine1")

  console.print(table)
