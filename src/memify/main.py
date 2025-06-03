#!/usr/bin/env python

import sys
import os
import argparse
from memify.flashcard import FlashcardSet
from memify.helpers import clear_screen, hide_cursor, display_centered_msg

def main():
    parser = argparse.ArgumentParser(description="Simple command-line flashcard program", formatter_class=lambda prog: argparse.HelpFormatter(prog, width=100, max_help_position=35))
    parser.add_argument("-s", "--study", nargs='?', const="None", default=False, choices=["None", "flipped", "f"], metavar="f/flipped", help="choose a flashcard set to study. Use 'f' or 'flipped' for back-first.")
    parser.add_argument("-q", "--quiz", action="store_true", help="quiz yourself on a flashcard set.")
    parser.add_argument("-r", "--remove-incorrect", action="store_true", help="remove all incorrect sets.")
    parser.add_argument("-p", "--path", type=str, help="path to set file or flashcard root directory.")
    parser.add_argument("-v", "--version", action="version", version="memify v0.1.0")
    args = parser.parse_args()

    if not (args.study or args.quiz or args.remove_incorrect):
        parser.print_help()
        sys.exit(1)

    clear_screen()
    hide_cursor()

    try:
        flashcard_obj = FlashcardSet()
        # Remove incorrect sets mode (no prompts, just do it)
        if args.remove_incorrect:
            flashcard_obj.remove_incorrect_sets(flashcard_obj.get_flashcards_root_dir(args))

        flashcard_set_path = flashcard_obj.get_flashcard_set_path(args)
        if not flashcard_set_path:
            clear_screen()
            display_centered_msg("No set chosen", "bold red", 1)
            sys.exit(1)

        flashcard_set = flashcard_obj.get_flashcard_set_path_from_file(flashcard_set_path)

        if os.path.basename(os.path.dirname(os.path.dirname(flashcard_set_path))) == ".incorrect":
            flashcard_set.is_incorrect_set = True

        if args.study:
            if args.study in ("flipped", "f"):
                flashcard_set.show_front = False
            flashcard_set.study()
        elif args.quiz:
            flashcard_set.quiz()

        clear_screen()
        print()
        display_centered_msg("Bye! Good luck :)", "bold spring_green1", 0)

    except KeyboardInterrupt:
        clear_screen()
        sys.exit(130)
    finally:
        print("\x1b[?25h", end="")  # Restore cursor

if __name__ == "__main__":
    main()
