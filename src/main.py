#!/usr/bin/env python

import sys
import os
import argparse
from flashcard import Flashcard
from helpers import clear_screen, hide_cursor, display_centered_msg, move_cursor_to_left_middle
from menu import Menu

def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--study", nargs='?', const="None", default=False, choices=["None", "flipped", "f"], metavar="f/flipped", help="choose a flashcard set to study. Supply 'f' or 'flipped' argument to start the cards with the back 'up'.")
        parser.add_argument("-q", "--quiz", action="store_true", help="choose a flashcard set to quiz yourself on.")
        parser.add_argument("-r", "--remove-incorrect", action="store_true", help="remove all incorrect sets.")
        parser.add_argument("-p", "--path", type=str, help="specify full path to file which holds a set.")
        args = parser.parse_args()

        if not (args.study or args.quiz or args.remove_incorrect):
            print("memify: missing operand")
            print("   usage: memify [-h] [-s] [-q] [-r] [-p FILEPATH]")
            sys.exit(1)

        clear_screen()
        hide_cursor()

        flcd = Flashcard("", "")
        if not args.path:
            if os.environ.get("FLASHCARD_SETS_PATH") is None:
                display_centered_msg("Please set FLASHCARD_SETS_PATH environment variable to the full path of your flashcards", "bold red", 1)
            directory = os.environ["FLASHCARD_SETS_PATH"]
            if not os.path.isdir(directory):
                display_centered_msg("Make sure your flashcard directory is there and FLASHCARD_SETS_PATH is set to the full path!", "bold red", 1)
            if args.remove_incorrect:
                flcd.remove_incorrect_sets(directory)
            directory = Menu.show_menu(directory)
        else:
            directory = args.directory
        if directory is None:
            clear_screen()
            display_centered_msg("No set chosen", "bold red", 1)
        basename = os.path.basename(os.path.dirname(os.path.dirname(directory)))
        if basename == ".incorrect":
            flcd.chose_incorrect = True
        flcd.parse_flashcard_file(directory)
        if args.study:
            if args.study == "flipped" or args.study == "f":
                print("args.study", args.study)
                flcd.show_question = False
            flcd.flashcard_study()
        elif args.quiz:
            flcd.flashcard_quiz()
        clear_screen()
        move_cursor_to_left_middle()
        display_centered_msg("Bye! Good luck :)", "bold spring_green1", 0)
    except(KeyboardInterrupt): # Catches Ctrl+C doesn't quite catch SIGINT, but good enough for now
        clear_screen()
        sys.exit(130)
    finally:
        print("\x1b[?25h", end="")  # Always restore cursor -- esp needed for macos

if __name__ == "__main__":
    main()
