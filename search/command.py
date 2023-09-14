# search_app/command.py

import fnmatch
import logging
import os
import pathlib
import typer
import rich
import npyscreen
import curses
from search.callbacks import (
    _some_log,
    info_callback,
    file_startswith,
    file_endswith,
    version_callback,
    )
from search.config import app
from search.logs import (
    log_file, 
    exception_factory
    )
from search.npyscreen_app import (
    CodeEditorApp,
    CodeEditor,
    )
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from search import __app_name__, __version__
from termcolor import colored
from typing import Optional


@app.command(help="Command to [bold yellow]find[/bold yellow] a file by it's name 🔍.")
def find(filename: str = typer.Argument(help="Name of file to [bold yellow]search[/bold yellow] for. :page_facing_up:", 
                                        metavar="FILENAME"),
        path: str = typer.Argument(default=pathlib.Path.home(), 
                                help="Directory path for the file to search."),
        startswith: str = typer.Option(default=None, 
                                        help="Search specific file with 'startswith' method :rocket:.", 
                                        is_eager=True, 
                                        callback=file_startswith), 
        endswith: str = typer.Option(default=None, 
                                    help="""Search specific file with 
                                    'endswith' method :sunrise_over_mountains:""", 
                                    is_eager=True, 
                                    callback=file_endswith)) -> None:
    # current path.
    curr_path = pathlib.Path(path)

    if curr_path.is_dir():
        # scan all root from user home root.
        scanning_directory = os.walk(curr_path, topdown=True)

        # iterate all directory.
        for root, dirs, files in scanning_directory:
            for file in files:
                is_same_file = fnmatch.fnmatchcase(file, filename)
                # filter file same as filename param.
                if is_same_file:
                    # join the root and file.
                    fullpath = os.path.join(
                        colored(root, "white"), 
                        colored(file, "yellow", attrs=['bold'])
                        )
                    print(fullpath)
        # do logging below,
        _some_log.info_log(message=f"Find '{filename}' file in '{path}' directory")
        rich.print(f"Find {filename} file [bold green]success![/bold green]")
        raise typer.Exit()
    else:
        _some_log.error_log(FileNotFoundError, f"File or Directory not found: {curr_path}")

@app.command(help="Command to [bold green]create[/bold green] new file followed by a path :cookie:.")
def create(filename: str = typer.Argument(metavar="FILENAME", 
                                        help="Name of file to [bold green]create[/bold green] a new one. :page_facing_up:"),
            path: str = typer.Argument(default=pathlib.Path.home(), 
                                    metavar="PATH", 
                                    help="Directory [bold blue]path[/bold blue] for file that has been created. :file_folder:")) -> None:
    # we convert the path param with Path class.
    curr_path = pathlib.Path(path)

    # check if directory exist.
    if curr_path.is_dir():
        # we join the path with filename value.
        real_path = os.path.join(curr_path, filename)
        # check if real path is exist.
        if os.path.exists(real_path):
            _some_log.error_log(FileExistsError, f"File exists: {real_path}")
        else:
            with open(os.path.join(curr_path, filename), 'x'):
                rich.print(f"[bold green]Success creating file[/bold green], {real_path}")
        
        # do logging below,
        _some_log.info_log(message=f"Create new '{real_path}' file")
        rich.print(f"Create {filename} file [bold green]success![/bold green]")
        raise typer.Exit()
    else:
        raise _some_log.error_log(FileNotFoundError, f"File or Directory not found: {curr_path}")
    
@app.command(help="Command to [bold]read[/bold] a file from a directory :book:.")
def read(filename: str = typer.Argument(metavar="FILENAME", 
                                        help="Name of file to read of. :page_facing_up:"),
        path: str = typer.Argument(default=pathlib.Path.home(), 
                                metavar="PATH", 
                                help="Directory path of file that want to read of. :file_folder:"),
        file_type: str = typer.Option(default="text", 
                                    is_flag=True, 
                                    help="The syntax type of the file to be displayed. :computer:")) -> None:
    # we convert the path param with Path class.
    curr_path = pathlib.Path(path)

    # check if directory exist.
    if curr_path.is_dir():
        # we join the path with filename value.
        real_path = os.path.join(curr_path, filename)
        # check if real path is exist.
        if os.path.exists(real_path):
            raise _some_log.error_log(FileExistsError, f"File exists: {real_path}")
        else:
            # check if the file is .txt
            if filename.endswith(".txt"):
                user_file = open(os.path.join(curr_path, filename), 'r')
                # we use panel for easy to read.
                rich.print(Panel(user_file.read(), title=f"{filename}", title_align="center", style="white"))
            else:
                with open(os.path.join(curr_path, filename), 'r') as file:
                    code_syntax = Syntax(file.read(), file_type, theme="dracula", line_numbers=True, padding=1)
                    Console.print(Panel(code_syntax, title=f"{filename}", title_align="center"))
        # do logging below,
        _some_log.info_log(message=f"Read '{real_path}' file")
        rich.print(f"Read {filename} file [bold green]success![/bold green]")
        raise typer.Exit()
    else:
        raise exception_factory(FileNotFoundError, f"File or Directory not found: {curr_path}")

@app.command(help="Command to [bold blue]write[/bold blue] one file :page_facing_up:")
def write() -> None:
        # running the app
        code_editor_app = CodeEditorApp()
        code_editor_app.run()
        form_editor = CodeEditor()
        # condition if user pick 'EXIT' earlier
        if not form_editor.filename.value or not form_editor.path.value:
            rich.print('See ya :wave:')
        else:
            _some_log.info_log(message=f"Create and write file")
            real_path = os.path.join(form_editor.path.value, form_editor.filename.value)
            rich.print(f"Write {real_path} file [bold green]success![/bold green]")
            raise typer.Exit()


@app.command(help="Command to [bold red]delete[/bold red] one or more file :eyes:.")
def delete(filename: str = typer.Argument(metavar="FILENAME", 
                                        help="Name of file to be deleted. :page_facing_up:"),
            path: str = typer.Argument(default=pathlib.Path.home(), 
                                    metavar="PATH", 
                                    help="Directory of file to be deleted. :file_folder:")) -> None:
    # we convert the path param with Path class.
    curr_path = pathlib.Path(path)

    # check if directory exist.
    if curr_path.is_dir():
        # we join the path with filename value.
        real_path = os.path.join(curr_path, filename)
        # check if real path is exist.
        if not os.path.exists(real_path):
            raise _some_log.error_log(FileNotFoundError, f"File or Directory not found: {real_path}")
        else:
             # create confirm, and if N then abort it.
            with typer.confirm("Are you sure want to delete it?", abort=True):
                # we remove the file.
                os.remove(real_path)
                rich.print(f"Success to delete {real_path} file.")
        # do logging below,
        _some_log.info_log(message=f"Delete '{real_path}' file")
        rich.print(f"Delete {filename} file [bold green]success![/bold green]")
        raise typer.Exit()
    else:
        raise _some_log.error_log(FileNotFoundError, f"File or Directory not found: {curr_path}")
    
# main function in here!
@app.callback()
def main(version: Optional[bool] = typer.Option(None, "--version", "-v", 
                                                help="Show version of search CLI.", 
                                                is_eager=True, 
                                                callback=version_callback),
         info: Optional[bool] = typer.Option(None, "--info", "-i", 
                                             help="Display info about the application", 
                                             is_eager=True, 
                                             callback=info_callback)) -> None: return



