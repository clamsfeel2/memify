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
        parser.add_argument("-r", "--remove-incorrect", action="store_true", help="remove all incorrect sets.")
        parser.add_argument("-f", "--filepath", type=str, help="specify full path to file which holds a set.")
        args = parser.parse_args()

        if not (args.study or args.quiz or args.remove_incorrect):
            print("memify: missing operand")
            print("   usage: memify [-h] [-s] [-q] [-r] [-f FILEPATH]")
            sys.exit(1)

        clear_screen()
        hide_cursor()

        flcd = Flashcard("", "", False, False)
        if not args.filepath:
            directory = os.environ["FLASHCARD_SETS_PATH"]
            if args.remove_incorrect:
                flcd.remove_incorrect_sets(directory)
                # os.sys.exit()
            directory = Menu.show_menu(directory)
        else:
            directory = args.directory

        basename = os.path.basename(os.path.dirname(os.path.dirname(directory)))
        if basename == ".incorrect":
            flcd.chose_incorrect = True
        flcd.parse_markdown(directory)
        if args.study:
            flcd.flashcard_study()
        elif args.quiz:
            flcd.flashcard_quiz()
    except (KeyboardInterrupt): # Catches Ctrl+C doesn't quite catch SIGINT, but good enough for now
        clear_screen()
        sys.exit(130)
    finally:
        print("\x1b[?25h", end="")  # Makes sure to always restore the cursor no matter what
