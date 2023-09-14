# search/config.py

import typer


# create typer object.
app = typer.Typer(help="[bold green]Easiest[/bold green] way to [bold yellow]find[/bold yellow], [bold]read[/bold], [bold green]create[/bold green], and [bold red]delete[/bold red] a file :file_folder:.", 
                pretty_exceptions_show_locals=False, 
                pretty_exceptions_enable=True,
                rich_markup_mode='rich')
