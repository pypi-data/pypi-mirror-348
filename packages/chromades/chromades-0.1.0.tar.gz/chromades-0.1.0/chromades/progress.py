from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
import time
import random
from rich.console import Console

console = Console()

def cool_progress_bar(total=100, description="Working..."):
    with Progress(
        SpinnerColumn(style="bold magenta"),
        "[progress.description]{task.description}",
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:

        task = progress.add_task(f"[green]{description}", total=total)

        for _ in range(total):
            time.sleep(random.uniform(0.02, 0.07))
            progress.update(task, advance=1)
