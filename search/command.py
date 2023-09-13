# search_app/command.py

import fnmatch
import logging
import os
import pathlib
import typer
import rich
import npyscreen
import curses

from datetime import date
from ascii_magic import AsciiArt
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from search import __app_name__, __version__
from termcolor import colored
from typing import Optional


# create typer object.
app = typer.Typer(help="[bold green]Easiest[/bold green] way to [bold yellow]find[/bold yellow], [bold]read[/bold], [bold green]create[/bold green], and [bold red]delete[/bold red] a file :file_folder:.", 
                pretty_exceptions_show_locals=False, 
                pretty_exceptions_enable=True,
                rich_markup_mode='rich')

def show_logo():
    print('\n')
    my_art = AsciiArt.from_image('SEARCH_v1.png')
    my_art.to_terminal()
    print('\n')

def log_file():
    fullpath = os.path.join(pathlib.Path.cwd(), 'search', 'logs')
    has_dir = os.path.isdir(fullpath)
    
    if has_dir:
        file_target = os.path.join(fullpath, 'log.txt')
        return file_target
    else:
        pathlib.Path(fullpath).mkdir(exist_ok=False)
        file_target = os.path.join(fullpath, 'log.txt')
        return file_target

# create factory for exception.
def exception_factory(exception, message: str):
    logging.basicConfig(filename=log_file(), filemode='a+', 
                            format='%(name)s | %(asctime)s %(levelname)s - %(message)s',
                            level=logging.ERROR)
    logging.info(message)
    return exception(message)

# create version callback function.
def version_callback(value: bool) -> None:
    if value:
        # do logging below,
        logging.basicConfig(filename=log_file(), filemode='a+', 
                            format='%(name)s | %(asctime)s %(levelname)s - %(message)s',
                            level=logging.INFO)
        logging.info("Looks for CLI version.")
        show_logo()
        # use print from rich module.
        rich.print(f"[bold]{__app_name__} version[/bold]: {__version__}")
        raise typer.Exit()

# cretae info callback function.
def info_callback(value: bool) -> None:
    if value:
        # do logging below,
        logging.basicConfig(filename=log_file(), filemode='a+', 
                            format='%(name)s | %(asctime)s %(levelname)s - %(message)s',
                            level=logging.INFO)
        logging.info("Looks for application info.")
        show_logo()
        # create long text
        output = f"""[yellow]{'*'*52}[bold]Creator Info[/bold]{'*'*52}[/yellow]\
                    \n\n[bold]Creator name[/bold]: Faisal Ramadhan\
                    \n[bold]Creator email[/bold]: faisalramadhan1299@gmail.com\
                    \n[bold]Creator github[/bold]: https://github.com/kolong-meja\
                    \n\n[yellow]{'*'*50}[bold]Application Info[/bold]{'*'*50}[/yellow]\
                    \n\n[bold]{__app_name__} version[/bold]: {__version__}\
                    \n[bold]Update on[/bold]: {date.today()}\
                """
        rich.print(output)
        raise typer.Exit()

def file_startswith(value: str) -> None:
    if value:
        # user home root.
        user_home_root = pathlib.Path.home()
        # scan all root from user home root.
        scanning_directory = os.walk(user_home_root, topdown=True)

        # iterate all directory.
        for root, dirs, files in scanning_directory:
            for file in files:
                # filter file same as filename param.
                if file.startswith(value):
                    # join the root and file.
                    root = colored(root, "white")
                    file = colored(file, "yellow", attrs=['bold'])
                    fullpath = os.path.join(root, file)
                    print(fullpath)
        
        # do logging below,
        logging.basicConfig(filename=log_file(), filemode='a+', 
                            format='%(name)s | %(asctime)s %(levelname)s - %(message)s',
                            level=logging.INFO)
        logging.info("Find a file with 'startswith' method")
        rich.print(f"Search file startswith '{value}' [bold green]success![/bold green]")
        raise typer.Exit()

def file_endswith(value: str) -> None:
    if value:
        # user home root.
        user_home_root = pathlib.Path.home()
        # scan all root from user home root.
        scanning_directory = os.walk(user_home_root, topdown=True)

        # iterate all directory.
        for root, dirs, files in scanning_directory:
            for file in files:
                # filter file same as filename param.
                if file.endswith(value):
                    # join the root and file.
                    root = colored(root, "white")
                    file = colored(file, "yellow", attrs=['bold'])
                    fullpath = os.path.join(root, file)
                    print(fullpath)
        
        # do logging below,
        logging.basicConfig(filename=log_file(), filemode='a+', 
                            format='%(name)s | %(asctime)s %(levelname)s - %(message)s',
                            level=logging.INFO)
        logging.info("Find a file with 'endswith' method")
        rich.print(f"Search file endswith '{value}' [bold green]success![/bold green]")
        raise typer.Exit()

@app.command(help="Command to [bold yellow]find[/bold yellow] a file by it's name 🔍.")
def find(filename: str = typer.Argument(help="Name of file to [bold yellow]search[/bold yellow] for. :page_facing_up:", 
                                        metavar="FILENAME"),
        path: str = typer.Argument(default=pathlib.Path.home(), 
                                help="Directory path for the file to search."),
        log: bool = typer.Option(default=False, 
                                help="Log the output into 'log.txt' file. :memo:", 
                                is_flag=True),
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
                # filter file same as filename param.
                if fnmatch.fnmatch(file, filename):
                    # join the root and file.
                    root = colored(root, "white")
                    file = colored(file, "yellow", attrs=['bold'])
                    fullpath = os.path.join(root, file)
                    print(fullpath)
    else:
        raise exception_factory(FileNotFoundError, f"File or Directory not found: {curr_path}")
    
    if log:
        # do logging below,
        logging.basicConfig(filename=log_file(), filemode='a+', 
                            format='%(name)s | %(asctime)s %(levelname)s - %(message)s',
                            level=logging.INFO)
        logging.info("Execute 'find' command to find a file by it's name.")
        rich.print(f"Find {filename} file [bold green]success![/bold green]")
        raise typer.Exit()

@app.command(help="Command to [bold green]create[/bold green] new file followed by a path :cookie:.")
def create(filename: str = typer.Argument(metavar="FILENAME", 
                                        help="Name of file to [bold green]create[/bold green] a new one. :page_facing_up:"),
            path: str = typer.Argument(default=pathlib.Path.home(), 
                                    metavar="PATH", 
                                    help="Directory [bold blue]path[/bold blue] for file that has been created. :file_folder:"),
            log: bool = typer.Option(default=False, 
                                    help="Log the output into 'log.txt' file. :memo:")) -> None:
    # we convert the path param with Path class.
    curr_path = pathlib.Path(path)

    # check if directory exist.
    if curr_path.is_dir():
        # we join the path with filename value.
        real_path = os.path.join(curr_path, filename)
        # check if real path is exist.
        if os.path.exists(real_path):
            raise exception_factory(FileExistsError, f"File exists: {real_path}")
        else:
            with open(os.path.join(curr_path, filename), 'x'):
                rich.print(f"[bold green]Success creating file[/bold green], {real_path}")
    else:
        raise exception_factory(FileNotFoundError, f"File or Directory not found: {curr_path}")
    
    if log:
        # do logging below,
        logging.basicConfig(filename=log_file(), filemode='a+', 
                            format='%(name)s | %(asctime)s %(levelname)s - %(message)s',
                            level=logging.INFO)
        logging.info("Execute 'create' command to create a file.")
        rich.print(f"Create {filename} file [bold green]success![/bold green]")
        raise typer.Exit()
@app.command(help="Command to [bold]read[/bold] a file from a directory :book:.")
def read(filename: str = typer.Argument(metavar="FILENAME", 
                                        help="Name of file to read of. :page_facing_up:"),
        path: str = typer.Argument(default=pathlib.Path.home(), 
                                metavar="PATH", 
                                help="Directory path of file that want to read of. :file_folder:"),
        log: bool = typer.Option(default=False, 
                                help="Log the output into 'log.txt' file. :memo:"),
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
        if not os.path.exists(real_path):
            raise exception_factory(FileExistsError, f"File exists: {real_path}")
        else:
            # check if the file is .txt
            if filename.endswith(".txt"):
                user_file = open(os.path.join(curr_path, filename), 'r')
                # we use panel for easy to read.
                rich.print(Panel(user_file.read(), title=f"{filename}", title_align="center", style="white"))
            else:
                with open(os.path.join(curr_path, filename), 'r') as file:
                    code_syntax = Syntax(file.read(), file_type, theme="dracula", line_numbers=True, padding=1)
                    console = Console()
                    console.print(Panel(code_syntax, title=f"{filename}", title_align="center"))
    else:
        raise exception_factory(FileNotFoundError, f"File or Directory not found: {curr_path}")
    
    if log:
        # do logging below,
        logging.basicConfig(filename=log_file(), filemode='a+', 
                            format='%(name)s | %(asctime)s %(levelname)s - %(message)s',
                            level=logging.INFO)
        logging.info("Execute 'read' command to read a file.")
        rich.print(f"Read {filename} file [bold green]success![/bold green]")
        raise typer.Exit()

@app.command(help="Command to [bold blue]write[/bold blue] one file :page_facing_up:")
def write(log: bool = typer.Option(default=False, help="Log the output into 'log.txt' file. :memo:")) -> None:
    # write your custom code editor here 
    class MyTestApp(npyscreen.NPSAppManaged):
        def onStart(self):
            self.appTheme = npyscreen.setTheme(CustomTheme)
            self.addForm("MAIN", CodeEditor, name="Code Editor V1")
    
    # test creating custom theme
    class CustomTheme(npyscreen.ThemeManager):
        default_colors = {
            'DEFAULT'     : 'CYAN_BLACK',
            'FORMDEFAULT' : 'YELLOW_BLACK',
            'NO_EDIT'     : 'GREEN_BLACK',
            'STANDOUT'    : 'CYAN_BLACK',
            'CURSOR'      : 'WHITE_BLACK',
            'CURSOR_INVERSE': 'BLACK_WHITE',
            'LABEL'       : 'GREEN_BLACK',
            'LABELBOLD'   : 'WHITE_BLACK',
            'CONTROL'     : 'GREEN_BLACK',
            'IMPORTANT'   : 'GREEN_BLACK',
            'SAFE'        : 'GREEN_BLACK',
            'WARNING'     : 'YELLOW_BLACK',
            'DANGER'      : 'RED_BLACK',
            'CRITICAL'    : 'BLACK_RED',
            'GOOD'        : 'GREEN_BLACK',
            'GOODHL'      : 'GREEN_BLACK',
            'VERYGOOD'    : 'BLACK_GREEN',
            'CAUTION'     : 'YELLOW_BLACK',
            'CAUTIONHL'   : 'BLACK_YELLOW',
        }
    
    # test creating custom MultiLineEdit
    """
    TODO: Create custom multilineedit
    """
    class CustomMultiLineEdit(npyscreen.MultiLineEdit):
        pass
        # def display_value(self, v1):
        #     lines = v1.split("\n")
        #     max_digits = len(str(len(lines)))
        #     numbered_lines = [f"{i+1:>{max_digits}} {line}" for i, line in enumerate(lines)]
        #     return '\n'.join(numbered_lines)

    # define our action form
    class CodeEditor(npyscreen.ActionForm):
        # define custom button text
        OK_BUTTON_TEXT = "SAVE"
        CANCEL_BUTTON_TEXT = "EXIT"

        def draw_title_and_help(self):
            if self.name:
                title = self.name[:(self.columns-4)]
                title = ' ' + str(title) + ' '
                if isinstance(title, bytes):
                    title = title.decode('utf-8', 'replace')
                self.add_line(0,58, 
                    title, 
                    self.make_attributes_list(title, curses.A_BOLD),
                    self.columns-4
                    )

        def create(self):
            self.filename = self.add(
                npyscreen.TitleFilename,
                begin_entry_at=18,
                name="Filename      :",
                relx=3,
                rely=2,
                )
            self.path = self.add(
                npyscreen.TitleText,
                begin_entry_at=18,
                value=str(pathlib.Path.home()),
                name="Folder Path   :",
                relx=3, 
                rely=4,
                editable=True
                )
            self.code = self.add(
                CustomMultiLineEdit,
                relx=2, 
                rely=6,
                editable=True,
                scroll_exit=True,
                )
        
        # add method for condition where user pick 'SAVE' button
        def on_ok(self):
            def save_code():
                if os.path.exists(self.path.value):
                    if self.filename.value.endswith('.txt'):
                        with open(os.path.join(self.path.value, self.filename.value), "a+") as file:
                            file.seek(0)
                            is_content_exist = file.read()

                            if is_content_exist:
                                file.write("\n"+self.code.value)
                            else:
                                file.write(self.code.value)
                            file.close()
                    else:
                        with open(os.path.join(self.path.value, self.filename.value), 'a+') as file:
                            file.seek(0)
                            is_code_exist = file.read()
                            
                            if is_code_exist:
                                file.write("\n\n"+self.code.value)
                            else:
                                file.write(f"# {self.filename.value}\n\n"+self.code.value)
                            file.close()
                else:
                    raise FileNotFoundError(f"Folder '{self.path.value}' not found")

            save_code()
            self.parentApp.setNextForm(None)
        
        # add method for condition where user pick 'EXIT' button
        def on_cancel(self):
            self.parentApp.setNextForm(None)
    
    # run the app
    App = MyTestApp()
    App.run()

    # print str message in certain condition
    form_data = CodeEditor()
    if not form_data.filename.value:
        rich.print(f"See ya bro! {form_data.filename.value} :wave:")
    else:
        rich.print(f"File '{form_data.filename.value}' written [bold green]successfully[/bold green]!")

    # do log if user input --log flag.
    if log:
        # do logging below,
        logging.basicConfig(filename=log_file(), filemode='a+', 
                            format='%(name)s | %(asctime)s %(levelname)s - %(message)s',
                            level=logging.INFO)
        logging.info("Execute 'write' command to write a file.")
        rich.print(f"Write {form_data.filename.value} file [bold green]success![/bold green]")
        raise typer.Exit()


@app.command(help="Command to [bold red]delete[/bold red] one or more file :eyes:.")
def delete(filename: str = typer.Argument(metavar="FILENAME", 
                                        help="Name of file to be deleted. :page_facing_up:"),
            path: str = typer.Argument(default=pathlib.Path.home(), 
                                    metavar="PATH", 
                                    help="Directory of file to be deleted. :file_folder:"),
            log: bool = typer.Option(default=False, 
                                    help="Log the output into 'log.txt' file. :memo:")) -> None:
    # we convert the path param with Path class.
    curr_path = pathlib.Path(path)

    # check if directory exist.
    if curr_path.is_dir():
        # we join the path with filename value.
        real_path = os.path.join(curr_path, filename)
        # check if real path is exist.
        if os.path.exists(real_path):
            # create confirm, and if N then abort it.
            with typer.confirm("Are you sure want to delete it?", abort=True):
                # we remove the file.
                os.remove(real_path)
                rich.print(f"Success to delete {real_path} file.")
        else:
            raise exception_factory(FileNotFoundError, f"File or Directory not found: {real_path}")
    else:
        raise exception_factory(FileNotFoundError, f"File or Directory not found: {curr_path}")

    if log:
        # do logging below,
        logging.basicConfig(filename=log_file(), filemode='a+', 
                            format='%(name)s | %(asctime)s %(levelname)s - %(message)s',
                            level=logging.INFO)
        logging.info("Execute 'delete' command to delete a file.")
        rich.print(f"Delete {filename} file [bold green]success![/bold green]")
        raise typer.Exit()
    
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



