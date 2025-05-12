import sys
import os

# add project root to Python's search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from views.start_screen import StartScreen
from views.quiz_screen import QuizScreen

def start_quiz(selected_category):
    sample_question = {
        "question": "Jaki jest największy ocean na świecie?",
        "answers": ["Atlantycki", "Spokojny", "Arktyczny", "Indyjski"],
        "correct_answer": "Spokojny"
    }
    quiz_window = QuizScreen(root, sample_question)

# Initialize main application window
root = tk.Tk()
root.withdraw()  # Hide the main window since StartScreen will open

start_screen = StartScreen()
start_screen.start_quiz = lambda: start_quiz(start_screen.selected_category.get())  # Call quiz with category selection

start_screen.mainloop()