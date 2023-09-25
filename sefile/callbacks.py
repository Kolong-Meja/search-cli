# search/callback.py

from sefile import (
    art,
    rich,
    typer,
    colored,
    os,
    pathlib,
    Progress,
    SpinnerColumn,
    TextColumn,
    __app_name__,
    __version__,
    __creator__,
    __creator_email__,
    __project_url__,
    )
from sefile.logs import CustomLog
from sefile.logs import exception_factory


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
        rich.print(f"[bold]{__app_name__} version[/bold]: {__version__}")
        raise typer.Exit()

# cretae info callback function.
def info_callback(value: bool) -> None:
    if value:
        # show logo
        ascii_art = art.text2art("SEFILE", font="swampland", chr_ignore=True)
        print(f"\n{colored(ascii_art, color='green', attrs=['bold'])}\n")
        # create long text
        output = f"""[yellow]{'*'*40}|[bold]Information[/bold]|{'*'*40}[/yellow]\
                    \n\n[bold]App name[/bold]: {__app_name__}\
                    \n[bold]{__app_name__} version[/bold]: {__version__}\
                    \n[bold]Creator name[/bold]: {__creator__}\
                    \n[bold]Creator email[/bold]: {__creator_email__}\
                    \n[bold]Creator github[/bold]: {__project_url__}\
                """
        rich.print(output)
        raise typer.Exit()

def auto_create_callback(value: bool) -> None:
    if value:
        curr_path = os.path.join(pathlib.Path.home(), "Create")
        if os.path.exists(curr_path):
            raise exception_factory(FileExistsError, f"Folder exists: {curr_path}")
        else:
            os.mkdir(curr_path)
            real_path = os.path.join(curr_path, 'main.py')
            if os.path.exists(real_path):
                raise exception_factory(FileExistsError, f"File exists: {real_path}")
            else:
                with open(real_path, 'w+') as file:
                    file.write(_code_example())
                    rich.print(f"[bold green]Success creating file[/bold green], {real_path}")

def file_startswith(value: str) -> None:
    if value:
        # user home root.
        user_home_root = pathlib.Path.home()
        # scan all root from user home root.
        scanning_directory = os.walk(user_home_root, topdown=True)
        file_total = 0
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
                        file_total += 1
                        # join the root and file.
                        root = f"[white]{root}[/white]"
                        file = f"[bold yellow]{file}[/bold yellow]"
                        fullpath = os.path.join(root, file)
                        rich.print(f"{fullpath}")
                        progress.advance(task)
        
        if file_total != 0:
            rich.print(f"Search file startswith '{value}' [bold green]success![/bold green]")
            raise typer.Exit()
        else:
            raise exception_factory(FileNotFoundError, f"File '{value}' not found.")

def file_endswith(value: str) -> None:
    if value:
        # user home root.
        user_home_root = pathlib.Path.home()
        # scan all root from user home root.
        scanning_directory = os.walk(user_home_root, topdown=True)
        file_total = 0
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
                        file_total += 1
                        root = f"[white]{root}[/white]"
                        file = f"[bold yellow]{file}[/bold yellow]"
                        # join the root and file.
                        fullpath = os.path.join(root, file)
                        rich.print(f"{fullpath}")
                        progress.advance(task)

        if file_total != 0:
            rich.print(f"Search file endswith '{value}' [bold green]success![/bold green]")
            raise typer.Exit()
        else:
            raise exception_factory(FileNotFoundError, f"File '{value}' not found.")
    