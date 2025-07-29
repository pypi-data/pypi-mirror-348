from rich.console import Console

console = Console()

def warning(text):
    console.print(f"[bold red]⚠️ WARNING: {text}[/]")

def success(text):
    console.print(f"[bold green]✅ {text}[/]")

def info(text):
    console.print(f"[bold cyan]{text}[/]")
