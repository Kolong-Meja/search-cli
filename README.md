# Search CLI

Search CLI is a personal project created by Faisal Ramadhan or myself. This project was built using the Python programming language. At the time of its creation, this CLI was only useful for finding the desired file according to the initial directory, but over time I started adding several new commands, such as Create, Read, and Delete. All of these commands have their own purpose and function.

## Requirements

Each project must have additional modules or packages for ease of project creation. I myself use a lot of packages to make this CLI. The modules or packages list that I use is:
* **fnmatch**

Info: if you want more information about this library, see https://docs.python.org/3/library/fnmatch.html
* **logging**

Info: if you want more information about this library, see https://docs.python.org/3/howto/logging.html
* **os**

Info: if you want more information about this library, see https://docs.python.org/3/library/os.html
* **pathlib**

Info: if you want more information about this library, see https://docs.python.org/3/library/pathlib.html
* **typer**

Installation:
```bash
python -m pip install "typer[all]"
```
Info: if you want more information about this library, see https://typer.tiangolo.com/tutorial/first-steps/
* **rich**

**WARNING**: If you do **pip install "typer[all]"** before, then you don't have to install the rich module.

Installation:
```bash
python -m pip install rich
```
Info: If you want more information about this library, see https://rich.readthedocs.io/en/stable/introduction.html
* **termcolor**

Installation: 
```bash
python -m pip install termcolor
```

Info: if you want more information about this library, see https://github.com/termcolor/termcolor
* **typing**

Info: if you want more information about this library, see https://docs.python.org/3/library/typing.html

## How to use it

It's quite easy, you just need to enter the command **python -m search --help**, then you get the output like this:

```bash
 Usage: search [OPTIONS] COMMAND [ARGS]...                                                                                             
                                                                                                                                       
 Easiest way to  find, read, create, and delete a file 📁.                                                                             
                                                                                                                                       
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Show version of search CLI.                                                                         │
│ --install-completion            Install completion for the current shell.                                                           │
│ --show-completion               Show completion for the current shell, to copy it or customize the installation.                    │
│ --help                          Show this message and exit.                                                                         │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ create            Command to create new file followed by a path 🍪.                                                                 │
│ delete            Command to delete one or more file 👀.                                                                            │
│ find              Command to find a file by it's name 🔍.                                                                           │
│ read              Command to read a file from a directory 📖.                                                                       │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### How to show CLI version?

```bash
python -m search --version
```

or

```bash
python -m search -v
```

### How to find a file?

```bash
python -m search find example.txt
```

or

Info: You can specify the initial directory path to find the file you want.
```bash
python -m search find example.txt /home/yourname/Documents
```

At first I created this based only on the filename, but eventually I added new flag options, namely --startswith and --endswith.

* **--startswith** flag is useful for searching files with your own custom prefix. Usage examples:

Info: **--startswith** flag has been set as **is_eager=True**, meaning this parameter will be executed and the main parameter will be overridden.
```bash
python -m search find --startswith=main
```

When you do this, the system will automatically look for files with a certain (in this case **main**) prefix from each directory or sub-directory that matches the initial directory.

* **--endswith** flag is useful for searching files with your own custome prefix. Usage examples:

Info: **--endswith** flag has been set as **is_eager=True**, meaning this parameter will be executed and the main parameter will be overridden.

```bash
ptyhon -m search find --endswith=.py
```

This flag has same functional as **--startswith** flag, but search file by the end name of the file that match with your custome prefix.

Info: you can also add your own initial path, example usage:

```bash
python -m search find --startswith=main /home
```

### How to create a file?

```bash
python -m search create example.txt
```
Info: Default directory set as **/home/username**

or 

```bash
python -m search create example.txt /home/username/Documents
```

The system will automatically create a file with a certain file type (according to the type you add at the end of the file) in the directory you enter.

### How to read a file?

```bash
python -m search read example.py /home
```

or 

```bash
python -m search read example.py /home --file-type=python
```

* **--file-type** flag is especially useful for reading files of a certain type. Default file typer set as **text** or **.txt**. Example of the output:

```python
# example.py

def my_func() -> None:
    print("Hello World!")
```

Info: this is just an example, the output will vary depending on the type of file you entered and the program in the file you entered

### How to delete a file?

```bash
python -m search delete example.py /home
```

You can add the path as you wish, but make sure that the files you delete are in your destination directory.

## Other useful things

You can add **--log** flag in every command. This flag is useful for creating a log for every action you take while running this CLI program. Including every error you get.

```bash
python -m search find example.py /home --log
```

This will create a new directory in your project directory named **logs**, and will add a file called **log.txt**. In this file you can monitor all your activities while running this program.

## Keep in mind

This program is only useful for **find, create, read, and delete**. Apart from that, I have nothing to add. I personally will only focus on the main command program, because there are still many things that can be updated in the future.