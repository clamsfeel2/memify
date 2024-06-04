import re
import os
import shutil
import sys
import random
from helpers import is_num, clear_screen, hide_cursor, move_cursor_to_middle_of_screen, move_cursor_to_left_middle, getch, check_differences
from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from rich.align import Align

class Flashcard:
    incorrect_answers = []
    flashcards = []
    file = None

    def __init__(self, question, answer, no_incorrect_cards = False, chose_incorrect = False):
        self.question = question
        self.answer = answer
        self.no_incorrect_cards = no_incorrect_cards
        self.chose_incorrect = chose_incorrect

    def apply_rich_format(self, text):
        """Applies Rich formatting to text"""
        text = re.sub(r"\\n", "\n", text)
        text = re.sub(r"\*\*(.*?)\*\*", r"[bold]\1[/bold]", text)
        text = re.sub(r"\*(.*?)\*", r"[italic]\1[/italic]", text)
        text = re.sub(r"\~\~(.*?)\~\~", r"[strike]\1[/strike]", text)
        text = re.sub(r"\_\_(.*?)\_\_", r"[underline]\1[/underline]", text)
        return text

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
                    current_question = self.apply_rich_format(title)
                elif level == 2:
                    current_answer = self.apply_rich_format(title)
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

    def remove_incorrect_sets(self, directory):
        incorrect_file_path = os.path.join(directory, ".incorrect")
        if os.path.exists(incorrect_file_path):
            shutil.rmtree(incorrect_file_path)
        else:
            console = Console()
            console.print(Text("\nYou have no incorrect sets to remove.\n"), justify="center", style="bold red")
        os.sys.exit()
 
    def output_incorrect_cards(self):
        """Outputs incorrect cards into .incorrect directory 
        located in root dir used for classes"""
        existing_data = []
        fullpath_to_classes = os.path.dirname(os.path.dirname(self.file))
        file_name = os.path.basename(self.file)
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
                quest = "# " + card.question
                ans = "## " + str(card.answer)
                # Check if the question and answer pair already exist in the file
                if any(quest in line and ans in line for line in existing_data):
                    continue
                out_file.write(quest + "\n" + ans + "\n")
        self.incorrect_answers = []

    # TODO: Clean this function tf up
    def flashcard_study(self):
        to_expand = True
        show_question = True
        console = Console()
        wanna_play = True
        total_flashcards = len(self.flashcards)

        clear_screen()
        hide_cursor()
        move_cursor_to_left_middle()

        console.print(Align.center("Time to study some flashcards!", style="medium_purple"))
        console.print(Align.center(f"[medium_purple underline]There are {total_flashcards} flashcards.[/medium_purple underline]"))
        console.print(Align.center(f"[medium_purple underline]Press q to quit.[/medium_purple underline]"))
        i = 0
        show_commands = True
        while wanna_play:
            while i < total_flashcards:
                key = None
                if key == "q" or key == "Q":
                    return
                show_question = True
                loop_over_one_card = True
                while loop_over_one_card:
                    card = self.flashcards[i]
                    card_details_text = card.question if show_question else card.answer # justify="center" to center align text
                    move_cursor_to_left_middle()
                    panel_title = f"Flashcard {i+1} of {total_flashcards}"
                    panel_subtitle = f"Question" if show_question else "Answer"
                    border_color = "bold blue" if show_question else "bold pale_violet_red1"
                    panel = Panel(card_details_text, title=panel_title, subtitle = panel_subtitle, title_align="left", subtitle_align="right", border_style=border_color, width=50, expand=to_expand)
                    console.print(Align.center(panel))
                    if show_commands:
                        console.print(Align.center("COMMANDS", style="bold turquoise2"))
                        console.print(Align.center("'c' to toggle this menu", style="turquoise2"))
                        console.print(Align.center("'any key' to flip the flashcard", style="turquoise2"))
                        console.print(Align.center("'enter' to go to the next card", style="turquoise2"))
                        console.print(Align.center("'b' to go to the previous card", style="turquoise2"))
                        console.print(Align.center("'q' to quit", style="turquoise2"))
                    else:
                        # move_cursor_to_left_middle(3)
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
                        loop_over_one_card = not loop_over_one_card
                    elif key in {"b", "B"}:
                        if i > 0:
                            i -= 1
                            loop_over_one_card = not loop_over_one_card
                    elif key in {"q", "Q"}:
                        clear_screen()
                        hide_cursor()
                        return
                    else:
                        clear_screen()
                        hide_cursor()
                        show_question = not show_question
            clear_screen()
            hide_cursor()
            move_cursor_to_left_middle()
            console.print(Align.center(Text("Study session completed! :)", justify="center"), style="bold spring_green1"))
            console.print(Text("\nPress ENTER to study again or ANY KEY to quit"), justify="center", end="", style="bold"); 
            user_answer = getch()
            if user_answer == "\r":
                i = 0
                wanna_play = True
                clear_screen()
                hide_cursor()
            else:
                wanna_play = False
                clear_screen()
                print("\x1b[H", end="", flush=True) # Move cursor back to top left of window

    def flashcard_quiz(self):
        wanna_play = True
        to_expand = True
        total_flashcards = len(self.flashcards)
        console = Console()
        clear_screen()
        console.print(Text(f"\nWelcome to the Flashcard Quiz! There are {total_flashcards} questions.\n"), justify="center", style="deep_sky_blue1")

        while wanna_play: 
            num_correct = 0
            num_wrong = 0
            clear_screen()
            for i, card in enumerate(self.flashcards, start=1):
                answered_correctly = False
                while not answered_correctly:  # Loop until the user answers correctly or quits
                    card_details_text = card.question
                    panel_title = f"Flashcard {i} of {total_flashcards}"
                    panel = Panel(card_details_text, title=panel_title, title_align="left", subtitle_align="right", border_style="bold blue", width=50, expand=to_expand)
                    console.print(Align.center(panel))

                    console.print(Text("Your answer\x1b[s"), justify="center", end=""); # \x1b[s saves cursor pos
                    user_answer = input("\x1b[u: ").strip().lower() # \x1b[u restores cursor pos so I can have the input in the middle of screen!

                    og_answer = card.answer;
                    everything_is_num = is_num(user_answer) and is_num(card.answer)
                    if everything_is_num:
                        user_answer = int(user_answer)
                        card_answer = int(card.answer)
                    else:
                        user_answer = user_answer.lower()
                        card_answer = card.answer.lower()
                    if user_answer == card_answer:
                        console.print(Text(f"Correct ✔️"), justify="center", style="bold spring_green1")
                        num_correct += 1
                        answered_correctly = True
                    elif check_differences(user_answer, card_answer):
                        if everything_is_num:
                            clear_screen()
                            console.print(Text("\nYou're within 3! Try again"), justify="center", style="bold red")
                        else:
                            clear_screen()
                            console.print(Text("\nOnly one letter is wrong! Try again"), justify="center", style="bold red")
                    else:
                        console.print(Text(f"❌"), justify="center", style="bold red")
                        console.print(f"The correct answer is, \"{og_answer}\"", justify="center", style="green")
                        self.incorrect_answers.append(Flashcard(card.question, card_answer))
                        num_wrong += 1
                        answered_correctly = True
            console.print(Text("\nQuiz completed!"), justify="center", style="bold spring_green1")
            content = (f"Number of correct answers: {num_correct}\n" + f"Number of incorrect answers: {num_wrong}")
            console.print(Panel(content, title="Results", border_style="bold blue", expand=to_expand))
            self.output_incorrect_cards()
            if self.no_incorrect_cards and self.chose_incorrect:
                console.print(Text("\nYou have no more incorrect flashcards!\n"), justify="center", style="bold spring_green1")
                wanna_play = False
            else:
                hide_cursor()
                # Gets user input, if they press enter they wanna quiz again
                console.print(Text("\nPress ENTER to study again or ANY KEY to quit"), justify="center", end="", style="bold"); 
                user_answer = getch()
                if user_answer == "\r":
                    wanna_play = True
                else:
                    wanna_play = False
