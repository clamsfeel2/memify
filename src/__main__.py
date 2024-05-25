#!/usr/bin/env python

import sys
import os
import argparse
from flashcard import Flashcard
from helpers import clear_screen, hide_cursor
from menu import Menu

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--study", action="store_true", help="choose a flashcard set to study.")
        parser.add_argument("-q", "--quiz", action="store_true", help="choose a flashcard set to quiz yourself on.")
        parser.add_argument("-f", "--filepath", type=str, help="specify full path to file which holds a set.")
        args = parser.parse_args()

        if not (args.study or args.quiz):
            print("memify: missing operand")
            print("   usage: memify [-h] [-s] [-q] [-d DIRECTORY]")
            sys.exit(1)

        clear_screen()
        hide_cursor()

        if not args.filepath:
            directory = os.environ["FLASHCARD_SETS_PATH"]
            directory = Menu.show_menu(directory)
        else:
            directory = args.directory

        flcd = Flashcard("", "")
        flcd.parse_markdown(directory)
        if args.study:
            flcd.flashcard_study()
        elif args.quiz:
            flcd.flashcard_quiz()
    except (KeyboardInterrupt): # Catches Ctrl+C does not catch SIGINT, but good enough for now
        clear_screen()
        sys.exit(130)
