import sys
import re
import os
import shutil
import random
from memify.menu import Menu
from memify.helpers import is_num, clear_screen, hide_cursor, move_cursor_to_left_middle, getch, is_close_enough, display_centered_msg, display_panel, apply_rich_format

# TODO
    # Clean up the Flashcard class.
        # move quiz and study out of the class into sep one
            # just figure out watcha wanna do there.

class Flashcard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

class FlashcardSet:
    def __init__(self):
        self.cards = []
        self.incorrect_cards = []
        self.show_front = True
        self.no_incorrect = False
        self.is_incorrect_set = False
        self.filepath = None

    def get_flashcards_root_dir(self, args):
        if args.path:
            return os.path.dirname(os.path.abspath(args.path))
        env_path = os.environ.get("FLASHCARD_SETS_PATH")
        if not env_path or not os.path.isdir(env_path):
            display_centered_msg("Set FLASHCARD_SETS_PATH environment variable to your flashcards directory.", "bold red", 1)
            sys.exit(1)
        return env_path

    def get_flashcard_set_path(self, args):
        if args.path:
            return args.path
        env_path = os.environ.get("FLASHCARD_SETS_PATH")
        if not env_path or not os.path.isdir(env_path):
            display_centered_msg("Set FLASHCARD_SETS_PATH environment variable to your flashcards directory.", "bold red", 1)
            sys.exit(1)
        menu = Menu()
        return menu.show_menu(env_path)

    def get_flashcard_set_path_from_file(self, filepath):
        _, ext = os.path.splitext(filepath)
        ext = ext.lower()
        if ext == ".md":
            return MarkdownFlashcardSet(filepath)
        elif ext == ".csv":
            return CSVFlashcardSet(filepath)
        else:
            raise ValueError(f"Unsupported flashcard format: {ext}")

    def remove_incorrect_sets(self, class_dir):
        incorrect_dir = os.path.join(class_dir, ".incorrect")
        if os.path.isdir(incorrect_dir):
            from simple_term_menu import TerminalMenu
            menu = TerminalMenu(["yes", "no"], menu_cursor_style=("fg_cyan", "bold"), menu_highlight_style=("fg_cyan", "bold"),)
            if menu == 0:
                shutil.rmtree(incorrect_dir)
                display_centered_msg("\nRemoved all incorrect sets :)\n", "bold spring_green1")
            display_centered_msg("\nExited.\n", "bold red", 1)
        else:
            display_centered_msg("\nNo incorrect sets found.\n", "bold red", 1)
        sys.exit()

    def __save_incorrect_cards(self):
        if not self.incorrect_cards:
            self.__remove_existing_incorrect_file()
            self.no_incorrect = True
            return

        incorrect_dir = self.__get_incorrect_dir()
        os.makedirs(incorrect_dir, exist_ok=True)
        incorrect_file = self.__get_incorrect_file_path(incorrect_dir)

        existing_entries = set()
        if os.path.isfile(incorrect_file):
            with open(incorrect_file, encoding="utf8") as f:
                existing_entries = set(f.readlines())

        with open(incorrect_file, "a", encoding="utf-8") as f:
            for card in self.incorrect_cards:
                entry = f"# {card.question.replace('\n', '\\n')}\n## {card.answer}\n"
                if entry not in existing_entries:
                    f.write(entry)
        self.incorrect_cards = []

    def __remove_existing_incorrect_file(self):
        incorrect_dir = self.__get_incorrect_dir()
        incorrect_file = self.__get_incorrect_file_path(incorrect_dir)
        if os.path.isfile(incorrect_file):
            os.remove(incorrect_file)

    def __get_incorrect_dir(self):
        if not self.filepath or not isinstance(self.filepath, str):
            raise ValueError("FlashcardSet.filepath is not set. Cannot determine incorrect directory.")
        base_dir = os.path.dirname(os.path.dirname(self.filepath))
        set_dir = os.path.basename(os.path.dirname(self.filepath))
        if os.path.basename(base_dir) == ".incorrect":
            base_dir = os.path.dirname(base_dir)
        return os.path.join(base_dir, ".incorrect", set_dir)

    def __get_incorrect_file_path(self, incorrect_dir):
        if not self.filepath or not isinstance(self.filepath, str):
            raise ValueError("FlashcardSet.filepath is not set. Cannot determine incorrect file path.")
        base_name = os.path.splitext(os.path.basename(self.filepath))[0]
        incorrect_file = f"incorrect_{base_name}.md" if not base_name.startswith("incorrect_") else f"{base_name}.md"
        return os.path.join(incorrect_dir, incorrect_file)

    # Study section
    def study(self):
        current_index = 0
        show_help_menu = False
        repeat_study = True
        total_cards = len(self.cards)
        show_question = self.show_front

        clear_screen()
        hide_cursor()
        move_cursor_to_left_middle()

        while repeat_study:
            while current_index < total_cards:
                card = self.cards[current_index]
                while True:
                    move_cursor_to_left_middle()
                    hide_cursor()
                    panel_title = f"Flashcard {current_index + 1} of {total_cards}"
                    panel_subtitle = "Question" if show_question else "Answer"
                    border = "bold blue" if show_question else "bold pale_violet_red1"
                    display_panel(card.question if show_question else card.answer, panel_title, panel_subtitle, border)
                    if show_help_menu:
                        self.__show_study_help()
                    key = getch()
                    if key is None: raise KeyboardInterrupt
                    if key in {"c", "C", "?"}:
                        show_help_menu = not show_help_menu
                    elif key in {"\r", "n", "N"}:
                        current_index += 1
                        show_question = self.show_front
                        clear_screen()
                        break
                    elif key in {"b", "B"}:
                        if current_index > 0: current_index -= 1
                        clear_screen()
                        break
                    elif key in {"q", "Q"}:
                        clear_screen()
                        return
                    else:
                        show_question = not show_question
                        clear_screen()
            self.__study_complete()
            key = getch()
            if key is None: raise KeyboardInterrupt
            elif key == "\r":
                current_index = 0
                clear_screen()
                hide_cursor()
            elif key == "q":
                repeat_study = False
                clear_screen()

    def __show_study_help(self):
        display_centered_msg("Help", "turquoise2")
        display_centered_msg("'c' to toggle help", "turquoise2")
        display_centered_msg("'n' or 'ENTER' next card", "turquoise2")
        display_centered_msg("'b' previous card", "turquoise2")
        display_centered_msg("Any other key: flip card", "turquoise2")
        display_centered_msg("'q' quit", "turquoise2")

    def __study_complete(self):
        clear_screen()
        hide_cursor()
        move_cursor_to_left_middle()
        display_centered_msg("Study session completed! :)", "bold spring_green1")
        display_centered_msg("\nPress [enter] to study again or [q] to quit.", "bold")

    # Quiz section
    def quiz(self):
        repeat_quiz = True
        total_cards = len(self.cards)
        while repeat_quiz:
            num_correct = 0
            num_incorrect = 0
            clear_screen()
            display_centered_msg(f"\nWelcome to the Flashcard Quiz! {total_cards} question{'s' if total_cards != 1 else ''}.\nPress any key to continue.", "bold deep_sky_blue1")
            getch()
            for idx, card in enumerate(self.cards, 1):
                while True:
                    display_panel(card.question, f"Flashcard {idx} of {total_cards}", "", "bold blue")
                    display_centered_msg("Your answer\x1b[s", "")
                    user_input = input("\x1b[u: ").strip().lower()
                    original_answer = card.answer
                    both_num = is_num(user_input) and is_num(card.answer)
                    if both_num:
                        user_input = int(user_input)
                        answer_value = int(card.answer)
                    else:
                        answer_value = card.answer.lower()
                    if user_input == answer_value:
                        display_centered_msg("\nCorrect 󰸞\n", "bold spring_green1")
                        num_correct += 1
                        break
                    elif is_close_enough(user_input, answer_value):
                        clear_screen()
                        display_centered_msg("\nClose! Try again.\n", "bold red")
                    else:
                        display_centered_msg("\n❌", "bold red")
                        display_centered_msg(f"\nCorrect answer: \"{original_answer}\"\n", "green")
                        self.incorrect_cards.append(Flashcard(card.question, card.answer))
                        num_incorrect += 1
                        break
            display_centered_msg("\nQuiz completed!", "bold spring_green1")
            display_panel(f"Correct: {num_correct}\nIncorrect: {num_incorrect}", "Results", "", "bold blue")
            self.__save_incorrect_cards()
            if self.no_incorrect and self.is_incorrect_set:
                display_centered_msg("\nNo more incorrect flashcards!\n", "bold spring_green1")
                repeat_quiz = False
            else:
                hide_cursor()
                display_centered_msg("\nPress [enter] to study again or [q] to quit.", "bold")
                while True:
                    key = getch()
                    if key == "\r":
                        repeat_quiz = True
                        break
                    elif key == "q":
                        repeat_quiz = False
                        break

class MarkdownFlashcardSet(FlashcardSet):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self.__parse_markdown(filepath)

    def __parse_markdown(self, filepath):
        with open(filepath, encoding="utf-8") as file:
            lines = file.read().splitlines()
        question, answer = None, None
        first_cards = []
        cards = []
        for line in lines:
            match = re.match(r"^(#+)\s+(.*)", line)
            if not match: continue
            level, text = len(match.group(1)), match.group(2)
            if level == 1:
                question = apply_rich_format(text)
            elif level == 2:
                answer = apply_rich_format(text)
            if question and answer:
                card = Flashcard(question.replace("FIRST_CARD ", "", 1) if question.startswith("FIRST_CARD") else question, answer)
                (first_cards if question.startswith("FIRST_CARD") else cards).append(card)
                question, answer = None, None
        random.shuffle(cards)
        self.cards = first_cards + cards

class CSVFlashcardSet(FlashcardSet):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self.__parse_csv(filepath)

    def __parse_csv(self, filepath):
        with open(filepath, encoding="utf-8") as file:
            values = [v.strip() for v in file.read().split(',')]
        first_cards = []
        cards = []
        for i in range(0, len(values) - 1, 2):
            question = apply_rich_format(values[i])
            answer = apply_rich_format(values[i + 1])
            if not question or not answer: continue
            card = Flashcard(question.replace("FIRST_CARD ", "", 1) if question.startswith("FIRST_CARD") else question, answer)
            (first_cards if question.startswith("FIRST_CARD") else cards).append(card)
        random.shuffle(cards)
        self.cards = first_cards + cards
