# search/callback.py

from sefile import (
    art,
    rich,
    typer,
    time,
    colored,
    dataclass,
    os,
    fnmatch,
    pathlib,
    Progress,
    SpinnerColumn,
    TextColumn,
    __app_name__,
    __version__,
    __creator__,
    __creator_email__,
    __project_url__,
    colors,
    Bullet,
    Input,
    Console,
    Panel,
    )
from sefile.exception import (
    InvalidFormat, 
    InvalidFileFormat
    )


@dataclass(frozen=True)
class _ProjectType:
    dir_path: str

    def __str__(self) -> None:
        return f"({self.dir_path})"
    
    def __repr__(self) -> None:
        return f"{self.__class__.__name__}({self.dir_path})"

    def _py_project(self) -> None:
        os.mkdir(self.dir_path)
        # create sub directory
        [os.makedirs(os.path.join(self.dir_path, subdir)) 
         for subdir in ["src", "tests"]]
        # create files in sub directory
        [open(os.path.join(os.path.join(self.dir_path, "src"), src_file), 'x') 
         for src_file in ["__init__.py", "main.py"]]
        # create files in sub directory
        [open(os.path.join(os.path.join(self.dir_path, "tests"), tests_file), 'x') 
         for tests_file in ["__init__.py", "test.py"]]
        # create required files for deployment
        [open(os.path.join(self.dir_path, req_file), 'x') 
         for req_file in ["LICENSE.md", "README.md", "requirements.txt"]]
        rich.print(f"All [bold green]Done![/bold green] ✅, path: '{self.dir_path}'")
    
    def _js_project(self) -> None:
        os.mkdir(self.dir_path)
        # create sub directory
        [os.makedirs(os.path.join(self.dir_path, subdir)) 
         for subdir in ["src", "tests", "public"]]
        # create files in sub directory
        [open(os.path.join(os.path.join(self.dir_path, "src"), src_file), "x") 
         for src_file in ["index.js", "app.js"]]
        # create files in sub directory
        [open(os.path.join(os.path.join(self.dir_path, "public"), public_file), "x") 
         for public_file in ["index.html", "style.css", "script.js"]]
        # create files in sub directory
        [open(os.path.join(os.path.join(self.dir_path, "tests"), tests_file), "x") 
         for tests_file in ["service.test.js", "component.test.js"]]
        # create required files for deployment
        [open(os.path.join(self.dir_path, req_file), "x") 
         for req_file in ["LICENSE.md", "README.md", "package.json"]]
        rich.print(f"All [bold green]Done![/bold green] ✅, path: {self.dir_path}")
    
    def _go_project(self) -> None:
        os.mkdir(self.dir_path)
        # create sub directory
        [os.makedirs(os.path.join(self.dir_path, subdir)) 
         for subdir in ["src", "tests"]]
        # create files in sub directory
        [open(os.path.join(os.path.join(self.dir_path, "src"), src_file), "x") 
         for src_file in ["main.go", "utils.go"]]
        # create files in sub directory
        [open(os.path.join(os.path.join(self.dir_path, "tests"), tests_file), "x") 
         for tests_file in ["test.go"]]
        # create required file for deployment
        [open(os.path.join(self.dir_path, req_file), "x") 
         for req_file in ["LICENSE.md", "README.md", "config.go"]]
        rich.print(f"All [bold green]Done![/bold green] ✅, path: {self.dir_path}")

@dataclass
class Callback:
    @staticmethod
    def _create_project(choice: str) -> None:
        # input project name
        project_name = Input(f"What's the name of the {choice} project? ", word_color=colors.foreground["yellow"])
        project_name_result = project_name.launch()
        if project_name_result.find("quit") != -1 or project_name_result.find("exit") != -1:
            print("See ya! 👋")
            raise typer.Exit()
        # input project directory
        project_dir = Input(f"Where do you want to save this {project_name_result}? ", word_color=colors.foreground["yellow"])
        project_dir_result = project_dir.launch()
        if project_dir_result.find("quit") != -1 or project_dir_result.find("exit") != -1:
            print("See ya! 👋")
            raise typer.Exit()
        # check if project dir exists in your PC
        if not pathlib.Path(project_dir_result).is_dir():
            raise FileNotFoundError(f"File or Path not found, path: '{project_dir_result}'")
        else:    
            project_path = os.path.join(project_dir_result, project_name_result)
        
        if os.path.exists(project_path):
            raise FileExistsError(f"Folder exists: '{project_path}'")
        else:
            if "Python" in choice:
                _python_project = _ProjectType(dir_path=project_path)
                _python_project._py_project()
            elif "Javascript" in choice:
                _javascript_project = _ProjectType(dir_path=project_path)
                _javascript_project._js_project()
            elif "Go" in choice:
                _golang_project = _ProjectType(dir_path=project_path)
                _golang_project._go_project()
            else:
                pass
    
    @staticmethod
    def _lazy_controller(user_input: str) -> None:
        # exit if user input 'quit' or 'exit'
        if user_input.find("quit") != -1 or user_input.find("exit") != -1:
            print("See ya! 👋")
            raise typer.Exit()
        # we must input all user input into sublist
        # so we can detect if user input more than 4 command
        _results = [[] for _ in range(4)]
        try:
            for i, value in enumerate(user_input.split()):
                _results[i].append(value)
        except:
            raise InvalidFormat(f"Invalid input format. Please use format: find <filename> from <path>, input: '{user_input}'")
        if len(_results[-1]) == 0:
            raise InvalidFormat(f"Invalid input format. Please use format: find <filename> from <path>, input: '{user_input}'")
        # then we flat the sublist into 1-dimensional list
        _flat_list = [subitem for item in _results for subitem in item]
        if _flat_list[0] != "find" or _flat_list[2] != "from":
            raise InvalidFormat(f"Invalid input format. Please use format: find <filename> from <path>, input: '{user_input}'")
        # if 2 (second) element does not have file type, it will be error.
        if _flat_list[1].find(".") == -1:
            raise InvalidFileFormat(f"Invalid file format, file: {_flat_list[1]}")
        # then we check if the path is a real directory or folder
        if (curr_path := pathlib.Path(_flat_list[-1])) and not curr_path.is_dir():
            raise FileNotFoundError(f"Directory '{_flat_list[-1]}' not found.")
        rich.print(f"System 🤖> [bold green]Allright[/bold green] we'll search [bold yellow]{_flat_list[1]}[/bold yellow] from [bold yellow]{_flat_list[-1]}[/bold yellow] for you\n")
        with Progress(
            SpinnerColumn(spinner_name="dots9"),
            TextColumn("[progress.description]{task.description}"),
            auto_refresh=True,
            transient=True,
            get_time=None,
        ) as progress:
            task = progress.add_task(f"Please wait for a moment...", total=100_000)
            similiar_files = [os.path.join(root, some_file) 
                             for root, dirs, files in os.walk(curr_path)
                             for some_file in filter(lambda f: fnmatch.fnmatchcase(f, _flat_list[1]), files)]
            for f in similiar_files:
                if os.path.getsize(f) != 0:
                    rich.print(f)
                    progress.advance(task)
        if len(similiar_files) < 1:
            raise FileNotFoundError(f"File {_flat_list[1]} not found.")
        else:
            rich.print(f"Find {_flat_list[1]} file [bold green]success![/bold green]")
            raise typer.Exit()

    def version_callback(self, value: bool) -> None:
        if value:
            ascii_art = art.text2art("SEFILE", font="swampland", chr_ignore=True)
            print(f"\n{colored(ascii_art, color='green', attrs=['bold'])}\n")
            rich.print(f"""[bold]App name[/bold]: {__app_name__}\
                    \n[bold]{__app_name__} version[/bold]: {__version__}\
                    \n[bold]Creator name[/bold]: {__creator__}\
                    \n[bold]Creator email[/bold]: {__creator_email__}\
                    \n[bold]Creator github[/bold]: {__project_url__}\
                    """)
            raise typer.Exit()
    
    def auto_create_callback(self, value: bool) -> None:
        if value:
            some_cli = Bullet(
                "What's simple project you want to create? ", 
                choices=["🐍 Python", "☕ Javascript", "🐼 Go", "❌ Cancel"],
                bullet=" >",
                margin=2,
                bullet_color=colors.bright(colors.foreground["cyan"]),
                background_color=colors.background["default"],
                background_on_switch=colors.background["default"],
                word_color=colors.foreground["white"],
                word_on_switch=colors.foreground["white"],
                )
            result = some_cli.launch()

            if result == "🐍 Python":
                Callback._create_project(choice=result)
            elif result == "☕ Javascript":
                Callback._create_project(choice=result)
            elif result == "🐼 Go":
                Callback._create_project(choice=result)
            else:
                print("See ya! 👋")
                raise typer.Exit()

    def lazy_search(self, value: bool) -> None:
        if value:
            user_input = Input(f"Command 😃> ", word_color=colors.foreground["yellow"])
            user_input_result = user_input.launch()
            Callback._lazy_controller(user_input=user_input_result)
    
    def startswith_search(self, value: str) -> None:
        if value:
            dir_start = Input(f"From where do you want to find '{value}' file? ", word_color=colors.foreground["yellow"])
            dir_start_result = dir_start.launch()
            if dir_start_result.find("quit") != -1 or dir_start_result.find("exit") != -1:
                print("See ya! 👋")
                raise typer.Exit()
            if not pathlib.Path(dir_start_result).is_dir():
                raise FileNotFoundError(f"File or Path not found, path: '{dir_start_result}'")
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
                                    for root, dirs, files in os.walk(dir_start_result, topdown=True)
                                    for some_file in filter(lambda f: f.startswith(value), files)]
                    for f in certain_files:
                        if os.path.getsize() != 0:
                            rich.print(f)
                            progress.advance(task)
                if len(certain_files) < 1:
                    raise FileNotFoundError(f"File startswith '{value}' not found from '{dir_start_result}' path")
                else:
                    rich.print(f"Search file startswith '{value}' [bold green]success![/bold green]")
                    raise typer.Exit()
    
    def endswith_search(self, value: str) -> None:
        if value:
            dir_start = Input(f"From where do you want to find '{value}' file? ", word_color=colors.foreground["yellow"])
            dir_start_result = dir_start.launch()
            if dir_start_result.find("quit") != -1 or dir_start_result.find("exit") != -1:
                print("See ya! 👋")
                raise typer.Exit()
            if not pathlib.Path(dir_start_result).is_dir():
                raise FileNotFoundError(f"File or Path not found, path: '{dir_start_result}'")
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
                                    for root, dirs, files in os.walk(dir_start_result, topdown=True)
                                    for some_file in filter(lambda f: f.endswith(value), files)]
                    for f in certain_files:
                        if os.path.getsize(f) != 0:
                            rich.print(f)
                            progress.advance(task)
                if len(certain_files) < 1:
                    raise FileNotFoundError(f"File endswith '{value}' not found from '{dir_start_result}' path")
                else:
                    rich.print(f"Search file startswith '{value}' [bold green]success![/bold green]")
                    raise typer.Exit()

