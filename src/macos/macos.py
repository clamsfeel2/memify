import os
import rumps
import subprocess 

def open_terminal_run_command(command):
    subprocess.run(['open', '-a', 'Terminal', '-n', '-e', command])

class AwesomeStatusBarApp(rumps.App):
    def __init__(self):
        super(AwesomeStatusBarApp, self).__init__("󱟱")  # Use the Nerd Font icon here
        self.directory = "/Users/Eli/Documents/Mollusk/Documents/Notes/Markdown/School/Spring2025/Flashcards"
        self.file_buttons = {}
        
        for file in os.listdir(self.directory):
            if file.endswith(".md"):
                file_name = file[:-3]  # Remove the last 3 characters (.md)
                full_path = os.path.join(self.directory, file)
                self.file_buttons[file_name] = full_path
                self.menu.add(rumps.MenuItem(file_name, callback=self.open_file))
        
        self.menu.add(rumps.MenuItem("Silly button", callback=self.open_file))
        self.menu.add(rumps.MenuItem("Say hi", callback=self.say_hi))
    
    def open_file(self, sender):
        full_path = self.file_buttons.get(sender.title, "")
        if full_path:
            subprocess.run(["memify", "-s", "-d", full_path])

    def toggle_button(self, sender):
        sender.state = not sender.state

    def say_hi(self, _):
        rumps.notification("Awesome title", "amazing subtitle", "hi!!1")

if __name__ == "__main__":
    print("")
    AwesomeStatusBarApp().run()
