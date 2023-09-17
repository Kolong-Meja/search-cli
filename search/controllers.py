# search/controllers.py

import fnmatch
import pathlib
import os
import rich
import inspect
import typer
from typing import Optional
from termcolor import colored
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from search.config import (
    app_level, 
    FileTypes
    )
from search.callbacks import _some_log
from search.logs import exception_factory
from search.npyscreen_app import (
    CodeEditorApp,
    CodeEditor,
    )


def find_logic(filename: str, path: str, startswith: str, endswith: str) -> None:
    # raise error if filename not include file type
    if filename.find(".") == -1:
        parameters = [param for param in inspect.signature(find_logic).parameters.keys()]
        raise ValueError(f"'{parameters[0]}' needs file type at the end, file: {filename}")

    # current path.
    curr_path = pathlib.Path(path)
    if curr_path.is_dir():
        # scan all root from user home root.
        scanning_directory = os.walk(curr_path, topdown=True)
        # append all file in empty list
        bunch_of_files = []
        # iterate all directory.
        for root, dirs, files in scanning_directory:
            for file in files:
                is_same_file = fnmatch.fnmatchcase(file, filename)
                # filter file same as filename param.
                if is_same_file:
                    # join the root and file.
                    fullpath = os.path.join(colored(root, "white"), colored(file, "yellow", attrs=['bold']))
                    # append file one by one
                    bunch_of_files.append(fullpath)
        
        for i, f in enumerate(bunch_of_files):
            print(f"{i+1}. {f}")
        # do logging below,
        """
        TODO: DEBUG IN HERE!
        """
        if app_level != 'development':
            _some_log.info_log(message=f"Find '{filename}' file in '{path}' directory")
        rich.print(f"Find {filename} file [bold green]success![/bold green]")
        raise typer.Exit()
    else:
        """
        TODO: DEBUG IN HERE!
        """
        if app_level != 'development':
            raise _some_log.error_log(FileNotFoundError, f"File or Directory not found: {curr_path}")
        else:
            raise exception_factory(FileNotFoundError, f"File or Directory not found: {curr_path}")

def create_logic(filename: Optional[str] = None, path: Optional[str] = None, auto: Optional[bool] = None) -> None:
    # raise error if filename not include file type
    if filename is not None and path is not None:
        if filename.find(".") == -1:
            parameters = [param for param in inspect.signature(create_logic).parameters.keys()]
            raise ValueError(f"'{parameters[0]}' needs file type at the end, file: {filename}")

        # we convert the path param with Path class.
        curr_path = pathlib.Path(path)
        # check if directory exist.
        if curr_path.is_dir():
            # we join the path with filename value.
            real_path = os.path.join(curr_path, filename)
            # check if real path is exist.
            if os.path.exists(real_path):
                """
                TODO: DEBUG IN HERE!
                """
                if app_level != 'development':
                    raise _some_log.error_log(FileExistsError, f"File exists: {real_path}")
                else:
                    raise exception_factory(FileExistsError, f"File exists: {real_path}")
            else:
                with open(os.path.join(curr_path, filename), 'x'):
                    rich.print(f"[bold green]Success creating file[/bold green], {real_path}")
            
            # do logging below,
            """
            TODO: DEBUG IN HERE!
            """
            if app_level != 'development':
                _some_log.info_log(message=f"Create new '{real_path}' file")
            rich.print(f"Create {filename} file [bold green]success![/bold green]")
            raise typer.Exit()
        else:
            """
            TODO: DEBUG IN HERE!
            """
            if app_level != 'development':
                raise _some_log.error_log(FileNotFoundError, f"File or Directory not found: {curr_path}")
            else:
                raise exception_factory(FileNotFoundError, f"File or Directory not found: {curr_path}")

def read_logic(filename: str, path: str, read_type: FileTypes) -> None:
    # raise error if filename not include file type
    if filename.find(".") == -1:
        parameters = [param for param in inspect.signature(read_logic).parameters.keys()]
        raise ValueError(f"'{parameters[0]}' needs file type at the end, file: {filename}")
    
    # we convert the path param with Path class.
    curr_path = pathlib.Path(path)
    # check if directory exist.
    if curr_path.is_dir():
        # we join the path with filename value.
        real_path = os.path.join(curr_path, filename)
        # check if real path is exist.
        if not os.path.exists(real_path):
            """
            TODO: DEBUG IN HERE!
            """
            if app_level != 'development':
                raise _some_log.error_log(FileExistsError, f"File not exists: {real_path}")
            else:
                raise exception_factory(FileExistsError, f"File not exists: {real_path}")
        else:
            # check if the file is .txt
            if filename.endswith(".txt"):
                user_file = open(os.path.join(curr_path, filename), 'r')
                # we use panel for easy to read.
                rich.print(Panel(user_file.read(), title=f"{filename}", title_align="center", style="white"))
            else:
                with open(os.path.join(curr_path, filename), 'r') as file:
                    code_syntax = Syntax(file.read(), read_type.value, theme="monokai", line_numbers=True, padding=1)
                    Console().print(Panel(code_syntax, title=f"{filename}", title_align="center"))
        # do logging below,
        """
        TODO: DEBUG IN HERE!
        """
        if app_level != 'development':
            _some_log.info_log(message=f"Read '{real_path}' file")
        rich.print(f"Read {filename} file [bold green]success![/bold green]")
        raise typer.Exit()
    else:
        """
        TODO: DEBUG IN HERE!
        """
        if app_level != 'development':
            raise _some_log.error_log(FileNotFoundError, f"File or Directory not found: {curr_path}")
        else:
            raise exception_factory(FileNotFoundError, f"File or Directory not found: {curr_path}")

def write_logic() -> None:
    # running the app
    code_editor_app = CodeEditorApp()
    code_editor_app.run()
    form_editor = CodeEditor()
    # condition if user pick 'EXIT' earlier
    if (not form_editor.filename.value or 
        not form_editor.path.value):
        rich.print('See ya :wave:')
    else:
        """
        TODO: DEBUG IN HERE!
        """
        app_level = os.environ.get('APP_LEVEL')
        if app_level != 'development':
            _some_log.info_log(message=f"Create and write file")
        real_path = os.path.join(form_editor.path.value, form_editor.filename.value)
        rich.print(f"Write {real_path} file [bold green]success![/bold green]")
        raise typer.Exit()

def delete_logic(filename: str, path: str) -> None:
    # raise error if filename not include file type
    if filename.find(".") == -1:
        parameters = [param for param in inspect.signature(delete_logic).parameters.keys()]
        raise ValueError(f"'{parameters[0]}' needs file type at the end, file: {filename}")

    # we convert the path param with Path class.
    curr_path = pathlib.Path(path)

    # check if directory exist.
    if curr_path.is_dir():
        # we join the path with filename value.
        real_path = os.path.join(curr_path, filename)
        # check if real path is exist.
        if not os.path.exists(real_path):
            """
            TODO: DEBUG IN HERE!
            """
            if app_level != 'development':
                raise _some_log.error_log(FileNotFoundError, f"File or Directory not found: {real_path}")
            else:
                raise exception_factory(FileNotFoundError, f"File or Directory not found: {real_path}")
        else:
            # create confirm, and if N then abort it.
            choice = typer.confirm("Are you sure want to delete it?", abort=True)
            # we remove the file.
            os.remove(real_path)
            rich.print(f"Success to delete {real_path} file.")
        # do logging below,
        """
        TODO: DEBUG IN HERE!
        """
        if app_level != 'development':
            _some_log.info_log(message=f"Delete '{real_path}' file")
        rich.print(f"Delete {filename} file [bold green]success![/bold green]")
        raise typer.Exit()
    else:
        """
        TODO: DEBUG IN HERE!
        """
        if app_level != 'development':
            raise _some_log.error_log(FileNotFoundError, f"File or Directory not found: {curr_path}")
        else:
            raise exception_factory(FileNotFoundError, f"File or Directory not found: {curr_path}")