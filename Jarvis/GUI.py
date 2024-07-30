import tkinter as tk
from tkinter import messagebox

# Initialize the Tkinter GUI
class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis Assistant")
        self.speak_command = None

        # Set up the GUI components
        self.label = tk.Label(root, text="Welcome to Jarvis Assistant", padx=80, pady=20)
        self.label.pack()

        self.button = tk.Button(root, text="Start", command=self.run_command)
        self.button.pack()

    def set_speak_command(self, command):
        self.speak_command = command

    def run_command(self):
        if self.speak_command:
            self.speak_command()

# Create Tkinter root and GUI instance
root = tk.Tk()
gui = JarvisGUI(root)
gui.set_speak_command(run_alpha)

# Start the GUI event loop
root.mainloop()
