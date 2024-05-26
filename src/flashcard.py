import re
import os
import sys
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

    def parse_markdown(self, filename):
        self.file = filename
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
                    current_question = title
                elif level == 2:
                    current_answer = title
                if current_answer and current_question:
                    self.flashcards.append(Flashcard(current_question, current_answer))
                    current_answer = None

    def output_incorrect_cards(self):
        fullpath_to_classes = os.path.dirname(os.path.dirname(self.file))
        existing_data = []

        if os.path.basename(fullpath_to_classes) == ".incorrect":
            fullpath_to_classes = os.path.dirname(fullpath_to_classes)
        file_name = os.path.basename(self.file)
        full_path_to_incorrect_sets = fullpath_to_classes + "/.incorrect/" + os.path.basename(os.path.dirname(self.file))

        incorrect_file_name = file_name if file_name.startswith("incorrect_") else "incorrect_" + file_name
        incorrect_file_path = full_path_to_incorrect_sets + "/" + incorrect_file_name
        if len(self.incorrect_answers) == 0 and os.path.isfile(incorrect_file_path):
            self.no_incorrect_cards = True
            os.remove(incorrect_file_path)
        # If the path {Flashcard_dir}/{.incorrect}/{Class_dir} does not exist create it
            # mkdirs acts like -P flag in mkdir command
        if not os.path.isdir(full_path_to_incorrect_sets):
            os.makedirs(full_path_to_incorrect_sets)
        if not self.no_incorrect_cards:
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
        self.incorrect_answers = [] # Reset incorrect cards so no multiples appear

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
            # for i in range(total_flashcards):
            while i < total_flashcards:
                key = None
                if key == "q" or key == "Q":
                    return
                show_question = True
                loop_over_one_card = True
                while loop_over_one_card:
                    card = self.flashcards[i]
                    center_text = Text(card.question if show_question else card.answer, justify="center")
                    move_cursor_to_left_middle()
                    panel_title = f"Flashcard {i+1} of {total_flashcards}"
                    panel_subtitle = f"Question" if show_question else "Answer"
                    border_color = "bold blue" if show_question else "bold pale_violet_red1"
                    panel = Panel(center_text, title=panel_title, subtitle = panel_subtitle, title_align="left", subtitle_align="right", border_style=border_color, width=50, expand=to_expand)
                    console.print(Align.center(panel))
                    if show_commands:
                        console.print(Align.center("COMMANDS (toggle with 'c')", style="turquoise2"))
                        console.print(Align.center("'any key' to flip the flashcard", style="turquoise2"))
                        console.print(Align.center("'enter' to go to the next card", style="turquoise2"))
                        console.print(Align.center("'b' to go to the previous card", style="turquoise2"))
                        console.print(Align.center("'q' to quit", style="turquoise2"))
                    else:
                        # move_cursor_to_left_middle(3)
                        sys.stdout.write("\033[J") # Clears from cursor to bottom of screen
                        sys.stdout.flush()
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
                wanna_play = True
                clear_screen()
            else:
                wanna_play = False
                clear_screen()
                print("\033[H", end="") # Move cursor back to top left of window

    def flashcard_quiz(self):
        wanna_play = True
        to_expand = True
        total_flashcards = len(self.flashcards)
        console = Console()
        print("\033c", end="")
        console.print(Text(f"\nWelcome to the Flashcard Quiz! There are {total_flashcards} questions.\n"), justify="center", style="deep_sky_blue1")

        while wanna_play: 
            num_correct = 0
            num_wrong = 0
            clear_screen()
            for i, card in enumerate(self.flashcards, start=1):
                answered_correctly = False
                while not answered_correctly:  # Loop until the user answers correctly or quits
                    center_text = Text(card.question, justify="center")
                    panel_title = f"Flashcard {i} of {total_flashcards}"
                    panel = Panel(center_text, title=panel_title, title_align="left", subtitle_align="right", border_style="bold blue", width=50, expand=to_expand)
                    console.print(Align.center(panel))

                    console.print(Text("Your answer\033[s"), justify="center", end=""); # \033[s saves cursor pos
                    user_answer = input("\033[u: ").strip().lower() # \033[u restores cursor pos so I can have the input in the middle of screen!

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
                        console.print(Text(f"The correct answer is, {card_answer}"), justify="center", style="bold red")
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
                # Gets user input, if they press enter they wanna quiz again
                console.print(Text("\nPress ENTER to study again or ANY KEY to quit"), justify="center", end="", style="bold"); 
                user_answer = getch()
                if user_answer == "\r":
                    wanna_play = True
                else:
                    wanna_play = False
