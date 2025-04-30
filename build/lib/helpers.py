import termios
import tty
import os
import sys
import re
from rich.console import Console
from rich.text import Text
from rich.align import Align
from rich.panel import Panel

# This is kinda overkill I think...
def is_num(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

### RICH HELPERS ###
def display_centered_msg(msg, color, exit_code = None, to_center_hztl_vtcl = False):
    console = Console()
    move_cursor_to_left_middle() if to_center_hztl_vtcl else ""
    console.print(Align.center(Text(msg, justify="center"), style=color))
    if exit_code is not None:
        sys.exit(exit_code)
    else:
        return 0

def display_panel(panel_txt, title_txt, subtitle_txt, border_color):
    console = Console()
    panel = Panel(panel_txt, title = title_txt, subtitle = subtitle_txt, title_align="left", subtitle_align="right", border_style=border_color, width=50)
    console.print(Align.center(panel))

def apply_rich_format(text):
    """Applies Rich formatting to text"""
    text = re.sub(r"\\n", "\n", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"[bold]\1[/bold]", text)
    text = re.sub(r"\*(.*?)\*", r"[italic]\1[/italic]", text)
    text = re.sub(r"\~\~(.*?)\~\~", r"[strike]\1[/strike]", text)
    text = re.sub(r"\_\_(.*?)\_\_", r"[underline]\1[/underline]", text)
    return text

### MANIPULATING SCREEN AND INPUT ###
def clear_screen():
    print("\x1bc", end="", flush=True)

def hide_cursor():
    print("\x1b[?25l", end="", flush=True)

def move_cursor_to_middle_of_screen():
    terminal_size = os.get_terminal_size()
    terminal_height = terminal_size.lines
    terminal_width = terminal_size.columns
    # Calculate the position for the cursor
    vertical_position = terminal_height // 2
    horizontal_position = terminal_width // 2
    # Move cursor to the middle of the screen on the farthest left side
    print(f"\x1b[{horizontal_position};{vertical_position}", end="", flush=True)

def move_cursor_to_left_middle():
    terminal_size = os.get_terminal_size()
    terminal_height = terminal_size.lines
    # Calculate the position for the cursor
    vertical_position = (terminal_height // 2)
    # Move cursor to the middle of the screen on the farthest left side
    print(f"\x1b[{vertical_position};0H", end="", flush=True)

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        # Check if Ctrl+C was pressed
        if ch == "\x03":
            return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

### DIFFS IN STRS AND NUMS ###
def check_differences(input1, input2):
    """Checks if string or number is different than answer"""
    diff_count = 0
    if isinstance(input1, str) and isinstance(input2, str):
        if len(input1) != len(input2):
            return False  # Different length strings cannot have one letter off
        input1 = input1.lower()
        input2 = input2.lower()
        for char1, char2 in zip(input1, input2):
            if char1.lower() != char2.lower():
                diff_count += 1
        return diff_count == 1
    if isinstance(input1, (int, float)) and isinstance(input2, (int, float)):
        if abs(input1 - input2) <= 3:
            return True
    return False
