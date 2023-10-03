# search/controllers.py

from sefile import (
    dataclass,
    os, 
    pathlib, 
    fnmatch, 
    rich,
    typer,
    Progress,
    SpinnerColumn,
    TextColumn,
    Optional,
    Panel,
    Syntax,
    shutil,
    Input,
    colors,
    )
from sefile.exception import (
    InvalidFileFormat, 
    InvalidFilename,
    InvalidPath,
    )

class Controller:
    __slots__ = ("filename", "path")

    def __init__(self, filename: Optional[str] = None, path: Optional[str] = None) -> None:
        self.filename = filename
        self.path = path

    def __str__(self) -> None:
        return f"('{self.filename}', '{self.path}')"

    def __repr__(self) -> None:
        return f"{self.__class__.__name__}('{self.filename}', '{self.path}')"

    # check if file has type at the end
    @staticmethod
    def _is_file(file_name: Optional[str] = None) -> None:
        if file_name is not None:
            if file_name.find(".") != -1:
                # ensure to execute next programs
                pass
            else:
                raise InvalidFileFormat(f"Invalid file format, file: {file_name}")
        else:
            raise InvalidFilename(f"Invalid filename, file: '{file_name}'")
    # to be implement in find_controller() method
    @staticmethod
    def _is_zero_total(total: int, file_name: str) -> None:
        if total < 1:
            raise FileNotFoundError(f"File '{file_name}' not found.")
        else:
            rich.print(f"Find {file_name} file [bold green]success![/bold green]")
            raise typer.Exit()

    # to be implement in read_controller() method    
    @staticmethod
    def _output_certain_file(
        file_name: str, 
        path: str, 
        format: str, 
        theme: str, 
        indent: bool = False
        ) -> None:
        if file_name.endswith(".txt"):
            with open(os.path.join(path, file_name), 'r') as user_file:
                rich.print(Panel(user_file.read(), title=f"{file_name}", title_align="center", style="white"))
        else:
            with open(os.path.join(path, file_name), 'r') as user_file:
                code_syntax = Syntax(
                    user_file.read(), 
                    format.value, 
                    theme=theme.value, 
                    line_numbers=True,
                    indent_guides=indent)
                curr_panel = Panel(code_syntax, title=f"{file_name}", title_align="center", border_style="yellow")
                rich.print(curr_panel)

    def find_controller(
        self, 
        startswith: str = None, 
        endswith: str = None, 
        lazy: Optional[bool] = None
        ) -> None:
        Controller._is_file(file_name=self.filename)
        if (curr_path := pathlib.Path(self.path)) and (curr_path.is_dir()):
            with Progress(
                SpinnerColumn(spinner_name="dots9"),
                TextColumn("[progress.description]{task.description}"),
                auto_refresh=True,
                transient=True,
            ) as progress:
                task = progress.add_task("Please wait for a moment...", total=100_000)
                similiar_files = [os.path.join(root, some_file) 
                             for root, dirs, files in os.walk(curr_path)
                             for some_file in filter(lambda f: fnmatch.fnmatchcase(f, self.filename), files)]
                for f in similiar_files:
                    if os.path.getsize(f) != 0:
                        rich.print(f)
                        progress.advance(task)
            Controller._is_zero_total(total=len(similiar_files), file_name=self.filename)
        else:
            raise FileNotFoundError(f"File or Directory not found: {curr_path}")

    def create_controller(self, project: Optional[bool] = None, write: Optional[bool] = None) -> None:
        if self.filename is not None and self.path is not None:
            Controller._is_file(file_name=self.filename)
            if (curr_path := pathlib.Path(self.path)) and (curr_path.is_dir()):
                if (real_path := os.path.join(curr_path, self.filename)) and (os.path.exists(real_path)):
                    raise FileExistsError(f"File exists: {real_path}")
                else:
                    with open(os.path.join(curr_path, self.filename), 'x'):
                        rich.print(f"[bold green]Success creating file[/bold green], {real_path}")
                
                rich.print(f"Create {self.filename} file [bold green]success![/bold green]")
                raise typer.Exit()
            else:
                raise FileNotFoundError(f"File or Directory not found: {curr_path}.")
        else:
            # ensure that the --auto callback is executed
            pass
    
    def read_controller(self, format: str, theme: str, indent: bool = False) -> None:
        Controller._is_file(file_name=self.filename)
        if (curr_path := pathlib.Path(self.path)) and (curr_path.is_dir()):
            if (real_path := os.path.join(curr_path, self.filename)) and not os.path.exists(real_path):
                raise FileNotFoundError(f"File not exists: {real_path}.")
            else:
                Controller._output_certain_file(
                    file_name=self.filename, 
                    path=curr_path, 
                    format=format, 
                    theme=theme, 
                    indent=indent
                    )

            rich.print(f"Read {self.filename} file [bold green]success![/bold green]")
            raise typer.Exit()
        else:
            raise FileNotFoundError(f"File or Directory not found: {curr_path}")
    
    def delete_controller(
        self,
        startswith: str = None, 
        endswith: str = None, 
        subfolder: bool = False
        ) -> None:
        if subfolder != False:
            if not self.path:
                raise InvalidPath(f"Invalid path, path: '{self.path}'.")
            if (curr_path := pathlib.Path(self.path)) and (curr_path.is_dir()):
                all_items = os.listdir(curr_path)
                subdirs = [d for d in all_items if os.path.isdir(os.path.join(curr_path, d))]
                rich.print(f"\n[bold green]{'[bold yellow] | [/bold yellow]'.join(subdirs)}[/bold green]\n")
                rich.print(f"There's {len(subdirs)} sub directory on '{curr_path}'.")
                subdir = Input(f"What sub directory you want to remove? ", word_color=colors.foreground["yellow"])
                subdir_result = subdir.launch()
                if subdir_result.find("quit") != -1 or subdir_result.find("exit") != -1:
                    print("See ya! 👋")
                    raise typer.Exit()
                else:
                    real_subdir = os.path.join(curr_path, subdir_result)
                    if not pathlib.Path(real_subdir).is_dir():
                        raise FileNotFoundError(f"Sub directory '{real_subdir}' not found.")
                    else:
                        removed_subdir = os.path.join(curr_path, subdir_result)
                        shutil.rmtree(removed_subdir)
                        rich.print(f"Sub directory '{removed_subdir}' [bold green]successfully removed![/bold green]")
                        raise typer.Exit()
        elif startswith:
            if self.path is None:
                raise InvalidPath(f"Invalid path, path: {self.path}")
            if not pathlib.Path(self.path).is_dir():
                raise FileNotFoundError(f"File or Path not found, path: '{self.path}'")
            else:
                with Progress(
                    SpinnerColumn(spinner_name="dots9"),
                    TextColumn("[progress.description]{task.description}"),
                    auto_refresh=True,
                    transient=True,
                    get_time=None,
                ) as progress:
                    task = progress.add_task(f"Please wait for a moment...", total=100_000)
                    certain_files = [os.path.join(root, some_file)
                                    for root, dirs, files in os.walk(self.path, topdown=True)
                                    for some_file in filter(lambda f: f.startswith(startswith), files)]
                    for f in certain_files:
                        if os.path.getsize(f) != 0:
                            rich.print(f)
                            progress.advance(task)
                if len(certain_files) < 1:
                    raise FileNotFoundError(f"File startswith '{startswith}' not found from '{self.path}' path")
                else:
                    rich.print(f"There's {len(certain_files)} files with '{startswith}' prefix")
                    choice = typer.confirm("Are you sure want to delete it?", abort=True)
                    for f in certain_files:
                        if os.path.isfile(f):
                            os.remove(f)
                    rich.print("All files removed successfully!")

        elif endswith:
            if self.path is None:
                raise InvalidPath(f"Invalid path, path: {self.path}")
            if not pathlib.Path(self.path).is_dir():
                raise FileNotFoundError(f"File or Path not found, path: '{self.path}'")
            else:
                with Progress(
                    SpinnerColumn(spinner_name="dots9"),
                    TextColumn("[progress.description]{task.description}"),
                    auto_refresh=True,
                    transient=True,
                    get_time=None,
                ) as progress:
                    task = progress.add_task(f"Please wait for a moment...", total=100_000)
                    certain_files = [os.path.join(root, some_file)
                                    for root, dirs, files in os.walk(self.path, topdown=True)
                                    for some_file in filter(lambda f: f.endswith(endswith), files)]
                    for f in certain_files:
                        if os.path.getsize(f) != 0:
                            rich.print(f)
                            progress.advance(task)
                if len(certain_files) < 1:
                    raise FileNotFoundError(f"File startswith '{endswith}' not found from '{self.path}' path")
                else:
                    rich.print(f"There's {len(certain_files)} files with '{endswith}' prefix")
                    choice = typer.confirm("Are you sure want to delete it?", abort=True)
                    for f in certain_files:
                        if os.path.isfile(f):
                            os.remove(f)
                    rich.print("All files removed successfully!")

        else:    
            Controller._is_file(file_name=self.filename)
            if (curr_path := pathlib.Path(self.path)) and (curr_path.is_dir()):
                if (real_path := os.path.join(curr_path, self.filename)) and not os.path.exists(real_path):
                    raise FileNotFoundError(f"File or Directory not found: {real_path}")
                else:
                    choice = typer.confirm("Are you sure want to delete it?", abort=True)
                    os.remove(real_path)
                    rich.print(f"Success to delete {real_path} file.")

                rich.print(f"Delete {self.filename} file [bold green]success![/bold green]")
                raise typer.Exit()
            else:
                raise FileNotFoundError(f"File or Directory not found: {curr_path}.")

