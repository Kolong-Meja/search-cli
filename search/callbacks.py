# search/callback.py

import pathlib
import os
import rich
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn
from search import __app_name__, __version__
from datetime import date
from ascii_magic import AsciiArt
from search.logs import CustomLog


def _code_example() -> str:
    output = """# create/main.py
                        
def main() -> None:
    pass
                        
if __name__ == '__main__':
    main()
    """
    return output

# define private instance for CustomLog class
_some_log = CustomLog(format_log='%(name)s | %(asctime)s %(levelname)s - %(message)s')

# create version callback function.
def version_callback(value: bool) -> None:
    if value:
        _some_log.info_log(message='Checking app version',)
        rich.print(f"[bold]{__app_name__} version[/bold]: {__version__}")
        raise typer.Exit()

# cretae info callback function.
def info_callback(value: bool) -> None:
    if value:
        _some_log.info_log(message='Checking app information')
        # show logo
        print('\n')
        AsciiArt.from_image(os.path.join(pathlib.Path.cwd(), 'search', 'SEARCH_v1.png')).to_terminal()
        print('\n')
        # create long text
        output = f"""[yellow]{'*'*52}[bold]Creator Info[/bold]{'*'*52}[/yellow]\
                    \n\n[bold]Creator name[/bold]: Faisal Ramadhan\
                    \n[bold]Creator email[/bold]: faisalramadhan1299@gmail.com\
                    \n[bold]Creator github[/bold]: https://github.com/kolong-meja\
                    \n\n[yellow]{'*'*50}[bold]Application Info[/bold]{'*'*50}[/yellow]\
                    \n\n[bold]App name[/bold]: {__app_name__}\
                    \n[bold]{__app_name__} version[/bold]: {__version__}\
                    \n[bold]Update on[/bold]: {date(year=2023, month=9, day=14)}\
                """
        rich.print(output)
        raise typer.Exit()

def auto_create_callback(value: bool) -> None:
    if value:
        curr_path = os.path.join(pathlib.Path.home(), "Create")
        if os.path.exists(curr_path):
            raise _some_log.error_log(FileExistsError, f"Folder exists: {curr_path}")
        else:
            os.mkdir(curr_path)
            real_path = os.path.join(curr_path, 'main.py')
            if os.path.exists(real_path):
                raise _some_log.error_log(FileExistsError, f"File exists: {real_path}")
            else:
                with open(real_path, 'w+') as file:
                    file.write(_code_example())
                    _some_log.info_log(message="Auto create file")
                    rich.print(f"[bold green]Success creating file[/bold green], {real_path}")
                    raise typer.Exit()

def file_startswith(value: str) -> None:
    if value:
        # user home root.
        user_home_root = pathlib.Path.home()
        # scan all root from user home root.
        scanning_directory = os.walk(user_home_root, topdown=True)
        # iterate all directory.
        with Progress(
            SpinnerColumn(spinner_name="dots9"),
            TextColumn("[progress.description]{task.description}"),
            auto_refresh=True, 
            transient=True,
            get_time=None,
            ) as progress:
            task = progress.add_task(f"Find file startswith '{value}' from {user_home_root}", total=100_000_000)
            for root, dirs, files in scanning_directory:
                for file in files:
                    # filter file same as filename param.
                    if file.startswith(value):
                        # join the root and file.
                        root = f"[white]{root}[/white]"
                        file = f"[bold yellow]{file}[/bold yellow]"
                        fullpath = os.path.join(root, file)
                        rich.print(f"{fullpath}")
                        progress.advance(task)
        
        # do logging below,
        _some_log.info_log(message=f"Find '{value}' file with '--startswith' flag.")
        rich.print(f"Search file startswith '{value}' [bold green]success![/bold green]")
        raise typer.Exit()

def file_endswith(value: str) -> None:
    if value:
        # user home root.
        user_home_root = pathlib.Path.home()
        # scan all root from user home root.
        scanning_directory = os.walk(user_home_root, topdown=True)
        with Progress(
            SpinnerColumn(spinner_name="dots9"),
            TextColumn("[progress.description]{task.description}"),
            auto_refresh=True, 
            transient=True,
            ) as progress:
            task = progress.add_task(f"Find file startswith '{value}' from {user_home_root}", total=100_000_000)
            # iterate all directory.
            for root, dirs, files in scanning_directory:
                for file in files:
                    # filter file same as filename param.
                    if file.endswith(value):
                        root = f"[white]{root}[/white]"
                        file = f"[bold yellow]{file}[/bold yellow]"
                        # join the root and file.
                        fullpath = os.path.join(root, file)
                        rich.print(f"{fullpath}")
                        progress.advance(task)
        
        # do logging below,
        _some_log.info_log(message=f"Find '{value}' file with '--endswith' flag.")
        rich.print(f"Search file endswith '{value}' [bold green]success![/bold green]")
        raise typer.Exit()