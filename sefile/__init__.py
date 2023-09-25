"""Top-Level package for search file"""
# search_app/__init__.py

import art
import fnmatch
import inspect
import logging
import npyscreen
import curses
import os
import pathlib
import rich
import time
import typer
from bullet import (
    colors,
    Bullet, 
    VerticalPrompt,
    SlidePrompt,
    Input,
    )
from enum import Enum
from termcolor import colored
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress, 
    SpinnerColumn, 
    TextColumn
    )
from rich.syntax import Syntax

# throw all information about this CLI below
__app_name__ = "Sefile CLI Tool"
__version__ = "1.0.2"
__creator__ = "Faisal Ramadhan"
__creator_email__ = "faisalramadhan1299@gmail.com"
__project_url__ = "https://github.com/kolong-meja"
