import termios
import tty
import os
import sys
import re
from rich.console import Console
from rich.text import Text
from rich.align import Align
from rich.panel import Panel

def is_num(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def display_centered_msg(message, color, exit_code=None, center_vertically=False):
    console = Console()
    if center_vertically:
        move_cursor_to_left_middle()
    console.print(Align.center(Text(message, justify="center"), style=color))
    if exit_code is not None:
        sys.exit(exit_code)
    return 0

def display_panel(text, title, subtitle, border_color):
    console = Console()
    panel = Panel(text, title=title, subtitle=subtitle, title_align="left", subtitle_align="right", border_style=border_color, width=50)
    console.print(Align.center(panel))

def apply_rich_format(text):
    text = re.sub(r"\\n", "\n", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"[bold]\1[/bold]", text)
    text = re.sub(r"\*(.*?)\*", r"[italic]\1[/italic]", text)
    text = re.sub(r"\~\~(.*?)\~\~", r"[strike]\1[/strike]", text)
    text = re.sub(r"\_\_(.*?)\_\_", r"[underline]\1[/underline]", text)
    return text

def clear_screen():
    print("\x1bc", end="", flush=True)

def hide_cursor():
    print("\x1b[?25l", end="", flush=True)

def move_cursor_to_left_middle():
    terminal_size = os.get_terminal_size()
    row = terminal_size.lines // 2
    print(f"\x1b[{row};0H", end="", flush=True)

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x03":  # Ctrl+C
            return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def is_close_enough(input1, input2):
    if isinstance(input1, str) and isinstance(input2, str):
        if len(input1) != len(input2):
            return False
        input1, input2 = input1.lower(), input2.lower()
        diff = sum(1 for a, b in zip(input1, input2) if a != b)
        return diff == 1
    if isinstance(input1, (int, float)) and isinstance(input2, (int, float)):
        return abs(float(input1) - float(input2)) <= 3
    return False
