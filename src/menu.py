import os
from simple_term_menu import TerminalMenu
from helpers import clear_screen

class Menu:
    @staticmethod
    def select_option(options, message):
        print(message)
        terminal_menu = TerminalMenu(options, menu_cursor_style=("fg_cyan", "bold"), menu_highlight_style=("fg_cyan", "bold"))
        menu_entry_index = terminal_menu.show()
        return options[menu_entry_index] if isinstance(menu_entry_index, int) else None

    @classmethod
    def show_menu(cls, directory):
        selected_class = cls.select_option([d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d)) and not d.startswith('.')], "Select a class")
        if selected_class:
            selected_set = cls.select_set_to_study(os.path.join(directory, selected_class))
            if selected_set:
                return selected_set
        return None

    @staticmethod
    def select_set_to_study(directory):
        diff_sets = {}
        for file in os.listdir(directory):
            if file.endswith(".md"):
                file_name = file[:-3]  # Remove the last 3 characters (.md)
                full_path = os.path.join(directory, file)
                diff_sets[file_name] = full_path

        if diff_sets:  # Ensure there's at least one file
            clear_screen()
            print("Select a set to study")
            terminal_menu = TerminalMenu(diff_sets.keys(), menu_cursor_style=("fg_cyan", "bold"), menu_highlight_style=("fg_cyan", "bold"))
            menu_entry_index = terminal_menu.show()

            if isinstance(menu_entry_index, int):
                selected_option = list(diff_sets.keys())[menu_entry_index]
                selected_file_path = diff_sets[selected_option]
                basename = os.path.basename(directory)
                incorrect_file_path = os.path.join(os.path.dirname(directory), ".incorrect", basename, "incorrect_" + selected_option + ".md")
            if os.path.exists(incorrect_file_path):
                view_incorrect = Menu.show_menu_to_view_incorrect()
                if view_incorrect == "yes":
                    return incorrect_file_path
        return selected_file_path

    @staticmethod
    def show_menu_to_view_incorrect():
        options = ["yes", "no"]
        clear_screen()
        print("Study incorect flashcards only?")
        terminal_menu = TerminalMenu(options, menu_cursor_style=("fg_cyan", "bold"), menu_highlight_style=("fg_cyan", "bold"))
        menu_entry_index = terminal_menu.show()
        return options[menu_entry_index]
