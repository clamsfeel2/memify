import re
import os
import shutil
import sys
import random
from helpers import is_num, clear_screen, hide_cursor, move_cursor_to_middle_of_screen, move_cursor_to_left_middle, getch, check_differences, display_centered_msg, display_panel, apply_rich_format

class Flashcard:
    incorrect_answers = []
    flashcards = []
    file = None

    def __init__(self, question, answer, show_question = True, no_incorrect_cards = False, chose_incorrect = False):
        self.question = question
        self.answer = answer
        self.show_question = show_question
        self.no_incorrect_cards = no_incorrect_cards
        self.chose_incorrect = chose_incorrect

    def parse_flashcard_file(self, filepath):
        """Parses the flashcard file based on its extension"""
        _, file_extension = os.path.splitext(filepath)
        if file_extension.lower() == ".md":
            self.parse_markdown(filepath)
        elif file_extension.lower() == ".csv":
            self.parse_csv(filepath)

    def parse_markdown(self, filename):
        """Parses markdown file and randomizes the order of 
        cards within a set"""
        self.file = filename
        tmp_flashcards = []
        with open(self.file, "r", encoding="utf-8") as file:
            markdown_text = file.read()
        current_question = None
        current_answer = None
        for line in markdown_text.split("\n"):
            match = re.match(r"^(#+)\s+(.*)", line)
            if match:
                level = len(match.group(1))
                title = match.group(2)
                if level == 1:
                    current_question = apply_rich_format(title)
                elif level == 2:
                    current_answer = apply_rich_format(title)
                if current_answer and current_question:
                    if re.match(r"^FIRST_CARD", current_question):
                        current_question = re.sub(r"^FIRST_CARD ", "", current_question)
                        tmp_flashcards.append(Flashcard(current_question, current_answer))
                        current_answer = None
                    else:
                        tmp_flashcards.append(Flashcard(current_question, current_answer))
                        current_question = None
                        current_answer = None
        random.shuffle(tmp_flashcards)
        self.flashcards.extend(tmp_flashcards)

    def parse_csv(self, filename):
        """Parses CSV file and randomizes the order of cards within a set"""
        self.file = filename
        tmp_flashcards = []
        first_card_flashcards = []
        with open(self.file, "r", encoding="utf-8") as file:
            combined_values = file.read().split(',')
            for i in range(0, len(combined_values), 2):  # Iterate pairs of values
                question = apply_rich_format(combined_values[i].strip())
                answer = apply_rich_format(combined_values[i + 1].strip())
                if question and answer:
                    if re.match(r"^FIRST_CARD", question):
                        question = re.sub(r"^FIRST_CARD ", "", question)
                        first_card_flashcards.append(Flashcard(question, answer))
                    else:
                        tmp_flashcards.append(Flashcard(question, answer))
        random.shuffle(tmp_flashcards)
        # Make sure first_card is at the beginning of flashcards
        self.flashcards = first_card_flashcards + tmp_flashcards

    def remove_incorrect_sets(self, directory):
        """Currently removes every incorrect set that it finds"""
        incorrect_file_path = os.path.join(directory, ".incorrect")
        if os.path.exists(incorrect_file_path):
            shutil.rmtree(incorrect_file_path)
            display_centered_msg("\nRemoved all incorrect sets :)\n", "bold spring_green1")
        else:
            display_centered_msg("\nYou have no incorrect sets to remove.\n", "bold red", 1) 
        os.sys.exit()
 
    def output_incorrect_cards(self):
        """Outputs incorrect cards into .incorrect directory 
        located in root dir used for classes"""
        existing_data = []
        fullpath_to_classes = os.path.dirname(os.path.dirname(self.file))
        file_name = os.path.splitext(os.path.basename(self.file))[0] + ".md"
        incorrect_file_name = file_name if file_name.startswith("incorrect_") else "incorrect_" + file_name
        if os.path.basename(fullpath_to_classes) == ".incorrect":
            fullpath_to_classes = os.path.dirname(fullpath_to_classes)
        full_path_to_incorrect_sets = os.path.join(fullpath_to_classes, ".incorrect", os.path.basename(os.path.dirname(self.file)))
        incorrect_file_path = os.path.join(full_path_to_incorrect_sets, incorrect_file_name)
        # Check if there are any incorrect answers to process
        if len(self.incorrect_answers) == 0:
            # If there are no incorrect answers check if incorrect file is there and remove it
            if os.path.isfile(incorrect_file_path):
                os.remove(incorrect_file_path)
            self.no_incorrect_cards = True
            return
        # Check that the directory structure exists
        if not os.path.isdir(full_path_to_incorrect_sets):
            os.makedirs(full_path_to_incorrect_sets)

        if os.path.isfile(incorrect_file_path):
            with open(incorrect_file_path, "r", encoding="utf8") as in_file:
                existing_data = in_file.readlines()

        with open(incorrect_file_path, "w", encoding="utf-8") as out_file:
            for card in self.incorrect_answers:
                # quest = "# " + card.question
                quest = "# " + card.question.replace("\n", "\\n")
                ans = "## " + str(card.answer)
                # Check if the question and answer pair already exist in the file
                if any(quest in line and ans in line for line in existing_data):
                    continue
                out_file.write(quest + "\n" + ans + "\n")
        self.incorrect_answers = []

    # TODO: Clean this function tf up
    def flashcard_study(self):
        i = 0
        show_commands = False
        wanna_play = True
        total_flashcards = len(self.flashcards)
        to_show_question = self.show_question

        clear_screen()
        hide_cursor()
        move_cursor_to_left_middle()

        while wanna_play:
            while i < total_flashcards:
                key = None
                if key == "q" or key == "Q":
                    return
                loop_over_one_card = True
                while loop_over_one_card:
                    card = self.flashcards[i]
                    card_details_text = card.question if to_show_question else card.answer
                    move_cursor_to_left_middle()
                    panel_title = f"Flashcard {i+1} of {total_flashcards}"
                    panel_subtitle = f"Question" if to_show_question else "Answer"
                    border_color = "bold blue" if to_show_question else "bold pale_violet_red1"
                    display_panel(card_details_text, panel_title, panel_subtitle, border_color)
                    if show_commands:
                        display_centered_msg("COMMANDS", "turquoise2")
                        display_centered_msg("'c' to toggle this menu", "turquoise2")
                        display_centered_msg("'any key' to flip the flashcard", "turquoise2")
                        display_centered_msg("'b' to go to the previous card", "turquoise2")
                        display_centered_msg("'q' to quit", "turquoise2")
                    else:
                        print("\x1b[J", end="", flush=True) # Clears from cursor to bottom of screen
                    key = getch()
                    if key is None:
                        raise KeyboardInterrupt

                    if key in {"c", "C"}:
                        show_commands = not show_commands
                    elif key == "\r":
                        clear_screen()
                        hide_cursor()
                        i += 1
                        loop_over_one_card = False
                        to_show_question = True if self.show_question else False
                    elif key in {"b", "B"}:
                        if i > 0:
                            i -= 1
                            loop_over_one_card = False
                    elif key in {"q", "Q"}:
                        clear_screen()
                        hide_cursor()
                        return
                    else:
                        clear_screen()
                        hide_cursor()
                        to_show_question = not to_show_question
            clear_screen()
            hide_cursor()
            move_cursor_to_left_middle()
            display_centered_msg("Study session completed! :)", "bold spring_green1")
            display_centered_msg("\nPress 'ANY KEY' to study again or 'ENTER' to quit.", "bold")
            user_answer = getch()
            if user_answer == "\r":
                wanna_play = False
                clear_screen()
                print("\x1b[H", end="", flush=True) # Move cursor back to top left of window
            else:
                i = 0
                wanna_play = True
                clear_screen()
                hide_cursor()

    def flashcard_quiz(self):
        wanna_play = True
        total_flashcards = len(self.flashcards)
        clear_screen()
        display_centered_msg(f"\nWelcome to the Flashcard Quiz! There {'is' if total_flashcards == 1 else 'are'} {total_flashcards} question{'s' if total_flashcards > 1 else ''}.\n Press any key to continue", "bold deep_sky_blue1")
        getch()

        while wanna_play: 
            num_correct = 0
            num_wrong = 0
            clear_screen()
            for i, card in enumerate(self.flashcards, start=1):
                answered_correctly = False
                while not answered_correctly:  # Loop until the user answers correctly or quits
                    display_panel(card.question, f"Flashcard {i} of {total_flashcards}", "", "bold blue")
                    display_centered_msg("Your answer\x1b[s", "")
                    user_answer = input("\x1b[u: ").strip().lower() # \x1b[u restores cursor pos so I can have the input in the middle of screen

                    og_answer = card.answer; # Saving to output og answer as card.answer is mutated within this method 
                    everything_is_num = is_num(user_answer) and is_num(card.answer)
                    if everything_is_num:
                        user_answer = int(user_answer)
                        card_answer = int(card.answer)
                    else:
                        user_answer = user_answer.lower()
                        card_answer = card.answer.lower()
                    if user_answer == card_answer:
                        display_centered_msg("Correct ✔️", "bold spring_green1")
                        num_correct += 1
                        answered_correctly = True
                    elif check_differences(user_answer, card_answer):
                        if everything_is_num:
                            clear_screen()
                            display_centered_msg("You're within 3! Try again.", "bold red")
                        else:
                            clear_screen()
                            display_centered_msg("Only one letter is wrong! Try again.", "bold red")
                    else:
                        display_centered_msg("❌", "bold red")
                        display_centered_msg(f"The correct answer is, \"{og_answer}\"", "green")
                        self.incorrect_answers.append(Flashcard(card.question, card_answer))
                        num_wrong += 1
                        answered_correctly = True
            display_centered_msg("\nQuiz completed!", "bold spring_green1")
            display_panel(f"Number of correct answers: {num_correct}\n" + f"Number of incorrect answers: {num_wrong}", "Results", "", "bold blue")
            self.output_incorrect_cards()
            if self.no_incorrect_cards and self.chose_incorrect:
                display_centered_msg("\nYou have no more incorrect flashcards!\n", "bold spring_green1")
                wanna_play = False
            else:
                hide_cursor()
                display_centered_msg("\nPress 'ANY KEY' to study again or 'ENTER' to quit", "bold")
                user_answer = getch()
                if user_answer == "\r":
                    wanna_play = False
                else:
                    wanna_play = True
