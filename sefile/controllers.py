# search/controllers.py

from sefile import (
    dataclass,
    os, 
    pathlib, 
    fnmatch, 
    inspect,
    rich,
    typer,
    Progress,
    SpinnerColumn,
    TextColumn,
    Optional,
    Console,
    Panel,
    Syntax,
    Group,
    Layout
    )
from sefile.config import FileTypes
from sefile.editor import CodeEditorApp
from sefile.exception import InvalidFileFormat


@dataclass(frozen=True)
class Controller:
    filename: Optional[str] = None
    path: Optional[str] = None

    def __str__(self) -> None:
        return f"('{self.filename}', '{self.path}')"

    def __repr__(self) -> None:
        return f"{self.__class__.__name__}('{self.filename}', '{self.path}')"

    # check if file has type at the end
    def _is_file(self, filename: str) -> None:
        if filename.find(".") != -1:
            # ensure to execute next programs
            pass
        else:
            raise InvalidFileFormat(f"Invalid file format, file: {filename}")
    # to be implement in find_controller() method
    def _is_zero_total(self, total: int, filename: str) -> None:
        if total < 1:
            raise FileNotFoundError(f"File '{filename}' not found.")
        else:
            rich.print(f"Find {filename} file [bold green]success![/bold green]")
            raise typer.Exit()

    # to be implement in read_controller() method    
    def _output_certain_file(self, filename: str, path: str, read_type: FileTypes) -> None:
        if filename.endswith(".txt"):
            with open(os.path.join(path, filename), 'r') as user_file:
                rich.print(Panel(user_file.read(), title=f"{filename}", title_align="center", style="white"))
        else:
            with open(os.path.join(path, filename), 'r') as user_file:
                code_syntax = Syntax(
                    user_file.read(), 
                    read_type.value, 
                    theme="monokai", 
                    line_numbers=True,
                    indent_guides=True)
                curr_panel = Panel(code_syntax, title=f"{filename}", title_align="center")
                rich.print(curr_panel)

    def find_controller(self, startswith: str, endswith: str, lazy: Optional[bool]) -> None:
        self._is_file(filename=self.filename)
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
            self._is_zero_total(total=len(similiar_files), filename=self.filename)
        else:
            raise FileNotFoundError(f"File or Directory not found: {curr_path}")

    def create_controller(self, auto: Optional[bool] = None) -> None:
        if self.filename is not None and self.path is not None:
            self._is_file(filename=self.filename)
            if (curr_path := pathlib.Path(self.path)) and (curr_path.is_dir()):
                if (real_path := os.path.join(curr_path, self.filename)) and (os.path.exists(real_path)):
                    raise FileExistsError(f"File exists: {real_path}")
                else:
                    with open(os.path.join(curr_path, self.filename), 'x'):
                        rich.print(f"[bold green]Success creating file[/bold green], {real_path}")
                
                rich.print(f"Create {self.filename} file [bold green]success![/bold green]")
                raise typer.Exit()
            else:
                raise FileNotFoundError(f"File or Directory not found: {curr_path}")
        else:
            # ensure that the --auto callback is executed
            pass
    
    def read_controller(self, read_type: FileTypes) -> None:
        self._is_file(filename=self.filename)
        if (curr_path := pathlib.Path(self.path)) and (curr_path.is_dir()):
            if (real_path := os.path.join(curr_path, self.filename)) and not os.path.exists(real_path):
                raise FileNotFoundError(f"File not exists: {real_path}")
            else:
                self._output_certain_file(filename=self.filename, path=curr_path, read_type=read_type)

            rich.print(f"Read {self.filename} file [bold green]success![/bold green]")
            raise typer.Exit()
        else:
            raise FileNotFoundError(f"File or Directory not found: {curr_path}")

    def write_controller() -> None:
        code_editor_app = CodeEditorApp()
        code_editor_app.run()
        rich.print('See ya :wave:')
        raise typer.Exit()
    
    def delete_controller(self, auto: Optional[bool] = None) -> None:
        self._is_file(filename=self.filename)
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
            raise FileNotFoundError(f"File or Directory not found: {curr_path}")
