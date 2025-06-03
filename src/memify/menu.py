import os
from simple_term_menu import TerminalMenu
from memify.helpers import clear_screen

class Menu:
    def quick_menu(self, options, prompt=None):
        if prompt: print(prompt)
        menu = TerminalMenu(options, menu_cursor_style=("fg_cyan", "bold"), menu_highlight_style=("fg_cyan", "bold"),)
        idx = menu.show()
        return idx if isinstance(idx, int) else None

    def show_menu(self, root_dir):
        if not os.path.isdir(root_dir): return None

        class_dirs = [
            dirname for dirname in os.listdir(root_dir)
            if os.path.isdir(os.path.join(root_dir, dirname)) and not dirname.startswith(".")
        ]
        selected_class = self.__select_option(class_dirs, "Select a class")
        if selected_class is None:
            return None

        class_path = os.path.join(root_dir, selected_class)
        while not any(fname.endswith((".md", ".csv")) for fname in os.listdir(class_path)):
            clear_screen()
            print(f"\x1b[1;31mNo sets in {selected_class}!\n\x1b[0mPick again.")
            selected_class = self.__select_option(class_dirs, "Select a class", False)
            if not selected_class: return None
            class_path = os.path.join(root_dir, selected_class)

        return self.__select_set(class_path)

    def __select_option(self, options, prompt, print_prompt=True):
        if print_prompt: print(prompt)
        idx = self.quick_menu(options)
        return options[idx] if idx is not None else None

    def __select_set(self, class_dir):
        flashcard_sets = {
            filename.rsplit('.', 1)[0]: os.path.join(class_dir, filename)
            for filename in os.listdir(class_dir)
            if filename.endswith((".md", ".csv"))
        }
        if not flashcard_sets: return None

        clear_screen()
        print("Select a set to study")
        options = list(flashcard_sets.keys())
        idx = self.quick_menu(options)
        if idx is None: return None

        selected_set_name = options[idx]
        set_file_path = flashcard_sets[selected_set_name]

        incorrect_set_path = os.path.join(os.path.dirname(class_dir), ".incorrect", os.path.basename(class_dir), f"incorrect_{selected_set_name}.md",)
        if os.path.exists(incorrect_set_path):
            if self.__ask_incorrect(): return incorrect_set_path

        return set_file_path

    def __ask_incorrect(self):
        clear_screen()
        print("Study incorrect flashcards only?")
        idx = self.quick_menu(["yes", "no"])
        return idx == 0
