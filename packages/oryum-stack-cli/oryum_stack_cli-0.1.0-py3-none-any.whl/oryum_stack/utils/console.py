from rich.console import Console

console = Console()

def success(message):
    console.print(f"[bold green]✔ {message}[/bold green]")

def info(message):
    console.print(f"[bold blue]ℹ {message}[/bold blue]")

def error(message):
    console.print(f"[bold red]✖ {message}[/bold red]")
