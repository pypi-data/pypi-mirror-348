from rich.console import Console
from rich.spinner import Spinner as RichSpinner
import time

console = Console()

class Spinner:
    def __init__(self, text="Loading..."):
        self.text = text
        self._spinner = RichSpinner("dots", text=self.text)

    def start(self, duration=5):
        with console.status(self.text):
            time.sleep(duration)
