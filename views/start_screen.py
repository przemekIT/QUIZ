import tkinter as tk
from tkinter import ttk, messagebox
from models.question_loader import load_questions, load_random_questions
from views.quiz_screen import QuizScreen
from views.result_history_screen import ResultHistoryScreen
import random

class StartScreen(tk.Tk):  
    def __init__(self):
        super().__init__()

        self.title("Quiz Wiedzy")
        self.geometry("600x400")
        self.configure(bg="#f4f4f4")  # ✅ Simple background color

        # ✅ Create UI elements
        self.create_widgets()

    def create_widgets(self):
        """Creates all UI elements for the start screen."""
        title_label = ttk.Label(self, text="Quiz Wiedzy", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)

        # ✅ Player Name Entry
        player_name_label = ttk.Label(self, text="Podaj swoje imię:", font=("Arial", 14))
        player_name_label.pack(pady=5)
        self.player_name_entry = ttk.Entry(self)
        self.player_name_entry.pack(pady=5)

        # ✅ Category Selection
        category_label = ttk.Label(self, text="Wybierz kategorię:", font=("Arial", 14))
        category_label.pack(pady=5)
        categories = ["Historia", "Nauka", "Kultura", "Losowy"]
        self.selected_category = tk.StringVar(value="Wybierz kategorię")
        self.category_dropdown = ttk.Combobox(self, values=categories, textvariable=self.selected_category)
        self.category_dropdown.pack(pady=5)
        self.category_dropdown.bind("<<ComboboxSelected>>", self.update_category)

        # ✅ Buttons
        ttk.Button(self, text="Rozpocznij Quiz", command=self.start_quiz).pack(pady=10)
        ttk.Button(self, text="Zobacz wyniki", command=self.show_results).pack(pady=10)
        ttk.Button(self, text="Wyjdź", command=self.quit).pack(pady=10)

    def update_category(self, event):
        """Update selected category."""
        self.selected_category.set(self.category_dropdown.get())

    def start_quiz(self):                
        """Starts the quiz with the selected category and player name."""
        chosen_category = self.selected_category.get().strip()
        player_name = self.player_name_entry.get().strip()

        if not chosen_category or chosen_category == "Wybierz kategorię":
            messagebox.showwarning("Błąd", "❌ Musisz wybrać kategorię!")
            return

        if not player_name:
            messagebox.showwarning("Błąd", "❌ Musisz wpisać imię gracza!")
            return

        questions = load_random_questions() if chosen_category == "Losowy" else load_questions(chosen_category)
        
        if questions:
            quiz_questions = random.sample(questions, min(len(questions), 20))
            self.withdraw()  
            quiz_window = QuizScreen(self, quiz_questions, player_name, chosen_category)
            quiz_window.grab_set() 
        else:
            messagebox.showwarning("Błąd", "Brak pytań dla tej kategorii.")

    def show_results(self):
        """Opens the results history window."""
        results_window = ResultHistoryScreen(self)
        results_window.grab_set()

if __name__ == "__main__":
    app = StartScreen()
    app.mainloop()