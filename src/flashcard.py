import re
import difflib
from pathlib import Path
from helpers import *
from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from rich.align import Align

class Flashcard:
    incorrect_answers = []
    flashcards = []
    file = None

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def parse_markdown(self, filename):
        flashcards = []
        self.file = filename
        with open(self.file, 'r') as file:
            markdown_text = file.read()

        current_question = None
        current_answer = None
        for line in markdown_text.split('\n'):
            match = re.match(r'^(#+)\s+(.*)', line)
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

        if os.path.basename(fullpath_to_classes) == ".incorrect":
            fullpath_to_classes = os.path.dirname(fullpath_to_classes)
        file_name = os.path.basename(self.file)
        fullpath_w_filename = self.file
        basename = os.path.basename(os.path.dirname(fullpath_w_filename))
        full_path_to_incorrect_sets = fullpath_to_classes + "/.incorrect/" + basename
        full_path_to_incorrect_file = full_path_to_incorrect_sets + "/" + file_name if file_name.startswith("incorrect_") else "incorrect_" + file_name
        # If there were no incorrect answers and the incorrect file exists remove it
        if len(self.incorrect_answers) == 0 and os.path.isfile(full_path_to_incorrect_file):
            os.remove(full_path_to_incorrect_file)
            sys.exit()
        # If the path {Flashcard_dir}/{.incorrect}/{Class_dir} does not exist create it
        # mkdirs acts like -P flag in mkdir command
        if not os.path.isdir(full_path_to_incorrect_sets):
            os.mkdirs(full_path_to_incorrect_sets)
        incorrect_file_name = file_name if file_name.startswith("incorrect_") else "incorrect_" + file_name
        incorrect_file_path = os.path.join(fullpath_to_classes, ".incorrect", incorrect_file_name)
        incorrect_file_path = full_path_to_incorrect_sets + "/" + incorrect_file_name
        with open(incorrect_file_path, "w") as out_file:
            for card in self.incorrect_answers:
                quest = "# " + card.question
                ans = "## " + str(card.answer) 
                out_file.write(quest + "\n" + ans + "\n")

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
        while wanna_play:
            for i in range(total_flashcards):
                key = None
                if key == "q" or key == "Q":
                    return
                card = self.flashcards[i]
                show_question = True
                while True:
                    center_text = Text(card.question if show_question else card.answer, justify="center")
                    move_cursor_to_left_middle()
                    panel_title = f"Flashcard {i+1} of {total_flashcards}"
                    panel_subtitle = f"Question" if show_question else "Answer"
                    border_color = "bold blue" if show_question else "bold pale_violet_red1"
                    panel = Panel(center_text, title=panel_title, subtitle = panel_subtitle, title_align="left", subtitle_align="right", border_style=border_color, width=50, expand=to_expand)
                    console.print(Align.center(panel))
                    console.print(Align.center("Press 'any key' to flip the flashcard, 'enter' to go to the next one, or 'q' to quit", style="turquoise2"))
                    key = getch()
                    if key is None:
                        raise KeyboardInterrupt
                    if key == "\r":
                        clear_screen()
                        hide_cursor()
                        break
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
            # print("\033[H", end='') # Move cursor back to top left of window
            console.print(Text("\nPress ENTER to study again or ANY KEY to quit"), justify="center", end="", style="bold"); 
            user_answer = getch()
            if user_answer == "\r":
                wanna_play = True
                clear_screen()
            else:
                wanna_play = False
                clear_screen()
                print("\033[H", end='') # Move cursor back to top left of window

    def flashcard_quiz(self):
        wanna_play = True
        to_expand = True
        total_flashcards = len(self.flashcards)
        total_questions = len(self.flashcards)
        console = Console()
        print("\033c", end='')
        console.print(Text(f"\nWelcome to the Flashcard Quiz! There are {total_questions} questions.\n"), justify="center", style="deep_sky_blue1")

        while wanna_play: 
            num_correct = 0
            num_wrong = 0
            clear_screen()
            # print("LEN:", len(self.flashcards))
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
                        # print("UA:", user_answer)
                        console.print(Text(f"❌"), justify="center", style="bold red")
                        console.print(Text(f"The correct answer is, {card_answer}"), justify="center", style="bold red")
                        self.incorrect_answers.append(Flashcard(card.question, card_answer))
                        num_wrong += 1
                        answered_correctly = True
            console.print(Text("\nQuiz completed!"), justify="center", style="bold spring_green1")
            content = (f"Number of correct answers: {num_correct}\n" + f"Number of incorrect answers: {num_wrong}")
            console.print(Panel(content, title="Results", border_style="bold blue", expand=to_expand))
            console.print(Text("\nPress ENTER to study again or ANY KEY to quit"), justify="center", end="", style="bold"); 
            user_answer = getch()
            if user_answer == "\r":
                wanna_play = True
            else:
                wanna_play = False
            self.output_incorrect_cards()
