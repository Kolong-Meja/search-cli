# tests/testing.py

from typer.testing import CliRunner

from search import __app_name__, __version__, command

# create CliRunner object.
runner = CliRunner()

def test_version():
    result = runner.invoke(command.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} version: {__version__}" in result.stdout

def test_find_file():
    # do some work here.
    pass

def test_log():
    # do some work here.
    pass