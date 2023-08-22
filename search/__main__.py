# search_app/__main__.py

from search import command, __app_name__

def main() -> None:
    command.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()