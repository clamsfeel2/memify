import tkinter as tk
import customtkinter
import random
import re
import os

ffont = "JetBrainsMonoNerdFont"

class Flashcard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

class FlashcardApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("memify")
        self.geometry("400x300")
        self.config(bg="#2E3440")
        self.flashcards = []
        self.current_card_index = 0
        self.flashcard_frame = tk.Frame(self, bg="#81A1C1", relief="raised", width=500, height=400)
        self.flashcard_frame.pack_propagate(0) # Prevents "flashcard" from resizing
        self.parse_flashcard_file(
                "/Users/Eli/Documents/Mollusk/Documents/Notes/Markdown/School/Summer2024/Flashcards/AmericanGov/gov_basics.md"
                ) # FIXME: Make prog search files not hardcode

        self.display_buttons()

    def display_buttons(self):
        # Create a frame to contain the label and buttons
        self.container_frame = tk.Frame(self, bg="#2E3440")
        self.container_frame.grid_columnconfigure(0, weight=1)

        self.container_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")

        # Create and place the welcome title
        self.label = tk.Label(self.container_frame, text="Welcome to Memify", bg="#2E3440", fg="#ECEFF4", font=(ffont, 20, "bold"))
        self.label.grid(row=3, column=0, pady=(50, 20)) 

        # Create and place the buttons
        study_button = customtkinter.CTkButton(self.container_frame, text="Study", command=self.study_flashcards)
        study_button.grid(row=4, column=0, pady=5)

        quiz_button = customtkinter.CTkButton(self.container_frame, text="Quiz", command=self.take_quiz)
        quiz_button.grid(row=5, column=0, pady=5)

        remove_button = customtkinter.CTkButton(self.container_frame, text="Remove incorrect sets", command=self.take_quiz)
        remove_button.grid(row=6, column=0, pady=5)

        # Place the container frame in the center of the window
        self.container_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.container_frame.pack()
        self.navigation_frame = tk.Frame(self, bg="#2E3440")

        # Buttons in study session
        self.back_button = customtkinter.CTkButton(self.navigation_frame, text="Back", command=self.show_prev_flashcard)
        self.back_button.grid(row=0, column=0, padx=5, pady=5)

        self.next_button = customtkinter.CTkButton(self.navigation_frame, text="Next", command=self.show_next_flashcard)
        self.next_button.grid(row=0, column=1, padx=5, pady=5)

        self.exit_button = customtkinter.CTkButton(self.navigation_frame, text="Exit", command=self.exit_flashcards)
        self.exit_button.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    def study_flashcards(self):
        if self.flashcards:
            self.flashcard_frame.pack(pady=20)
            self.show_flashcard(self.current_card_index)
            self.navigation_frame.pack(pady=10)
        else:
            messagebox.showinfo("No Flashcards", "No flashcards available to study.")


    def show_flashcard(self, index, x=False):
        self.bind("<Return>", lambda event: self.show_next_flashcard())
        self.bind("b", lambda event: self.show_prev_flashcard())
        self.label.pack_forget()
        self.container_frame.pack_forget()

        flashcard = self.flashcards[index]

        bg_color = "#81A1C1" if flashcard.question else "#FF87AF"

        if not hasattr(self, "card_label"):
            self.flashcard_counter_label = tk.Label(self.flashcard_frame, text=f"Flashcard {index+1} of {len(self.flashcards)}", font=(ffont, 10), padx=10, pady=5, bg=bg_color, fg="white")
            self.card_label = tk.Label(self.flashcard_frame, text=flashcard.question, font=(ffont, 12), padx=10, pady=10, bg=bg_color, fg="#ECEFF4", relief="raised", wraplength=450, anchor="w", justify="left")
            self.card_label.pack(expand=True, fill="both")
            self.flashcard_counter_label.pack(side="top", anchor="n", padx=10, pady=10)
        else:
            self.flashcard_counter_label.config(text=f"Flashcard {index+1} of {len(self.flashcards)}", bg=bg_color)
            self.card_label.config(text=flashcard.question, bg=bg_color, anchor="w")

        def flip_card(event=None):
            if self.card_label.cget("text") == flashcard.question:
                self.card_label.config(text=flashcard.answer, bg="#FF87AF", anchor="center")
            else:
                self.card_label.config(text=flashcard.question, bg="#81A1C1", anchor="w")


        self.card_label.bind("<Button-1>", flip_card)
        self.card_label.bind("<Key>", lambda event: flip_card() if event.char not in ["b", "\r"] else None)
        self.card_label.focus_set()  # Makes sure the label receives keyboard events

    def exit_flashcards(self):
        self.flashcard_frame.pack_forget()
        self.navigation_frame.pack_forget()
        self.exit_button.pack_forget()
        self.display_buttons()

    def take_quiz(self):
        pass

    def remove_incorrect_sets(self):
        pass

    def parse_flashcard_file(self, filepath):
        _, file_extension = os.path.splitext(filepath)
        if file_extension.lower() == ".md":
            self.parse_markdown(filepath)
        elif file_extension.lower() == ".csv":
            self.parse_csv(filepath)

    def parse_markdown(self, filename):
        self.file = filename
        tmp_flashcards = []
        first_card_flashcards = []
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
                    current_question = title.replace("\\n", "\n")
                elif level == 2:
                    current_answer = title.replace("\\n", "\n")
                if current_answer and current_question:
                    if current_question.startswith("FIRST_CARD"):
                        current_question = current_question.replace("FIRST_CARD ", "")
                        first_card_flashcards.append(Flashcard(current_question, current_answer))
                        current_answer = None
                    else:
                        tmp_flashcards.append(Flashcard(current_question, current_answer))
                        current_question = None
                        current_answer = None
        random.shuffle(tmp_flashcards)
        self.flashcards = first_card_flashcards + tmp_flashcards


    def parse_csv(self, filename):
        self.file = filename
        tmp_flashcards = []
        first_card_flashcards = []
        with open(self.file, "r", encoding="utf-8") as file:
            combined_values = file.read().split(',')
            for i in range(0, len(combined_values), 2):
                question = combined_values[i].strip()
                answer = combined_values[i + 1].strip()
                if question and answer:
                    if question.startswith("FIRST_CARD"):
                        question = question.replace("FIRST_CARD ", "")
                        first_card_flashcards.append(Flashcard(question, answer))
                    else:
                        tmp_flashcards.append(Flashcard(question, answer))
        random.shuffle(tmp_flashcards)
        self.flashcards = first_card_flashcards + tmp_flashcards

    def show_next_flashcard(self):
        if self.current_card_index == len(self.flashcards) - 1:
            return
        self.current_card_index = (self.current_card_index + 1) % len(self.flashcards)
        self.show_flashcard(self.current_card_index, True)

    def show_prev_flashcard(self):
        if self.current_card_index == 0:
            return
        self.current_card_index = (self.current_card_index - 1) % len(self.flashcards)
        self.show_flashcard(self.current_card_index)


def main():
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("green")  # blue, dark-blue, green
    app = FlashcardApp()
    app.geometry("500x300")
    app.mainloop()

if __name__ == "__main__":
    main()
