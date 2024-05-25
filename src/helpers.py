import termios
import tty
import os
import sys

# This is kinda overkill I think...
def is_num(x):
    # Removes neg sign and decimal -- don't need values, literally just checking if the value is a number
    without_sign = x.lstrip('-')
    without_decimal = without_sign.replace('.', '', 1)
    if without_decimal.isnumeric():
        return True
    else:
        return False

### MANIPULATING SCREEN AND INPUT ###
def clear_screen():
    print("\033c", end='')

def hide_cursor():
    print('\033[?25l', end="")

def move_cursor_to_middle_of_screen():
    terminal_size = os.get_terminal_size()
    terminal_height = terminal_size.lines
    terminal_width = terminal_size.columns
    # Calculate the position for the cursor
    vertical_position = terminal_height // 2
    horizontal_position = terminal_width // 2
    # Move cursor to the middle of the screen on the farthest left side
    print(f"\033[{horizontal_position};{vertical_position}", end='') 

def move_cursor_to_left_middle():
    terminal_size = os.get_terminal_size()
    terminal_height = terminal_size.lines
    # Calculate the position for the cursor
    vertical_position = terminal_height // 2
    # Move cursor to the middle of the screen on the farthest left side
    print(f"\033[{vertical_position};0H", end='') 

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        # Check if Ctrl+C was pressed
        if ch == '\x03':
            return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

### STRINGS AND NUMS ###
def check_differences(input1, input2):
    diff_count = 0
    if isinstance(input1, str) and isinstance(input2, str):
        if len(input1) != len(input2):
            return False  # Different length strings cannot have one letter off
        for char1, char2 in zip(input1, input2):
            if char1.lower() != char2.lower():
                diff_count += 1
        return diff_count == 1
    elif isinstance(input1, (int, float)) and isinstance(input2, (int, float)):
        if abs(input1 - input2) <= 3:
            return True
    return False
