import tkinter as tk
from tkinter import ttk
from models.question_loader import load_questions
from views.quiz_screen import QuizScreen

class StartScreen(tk.Tk):  
    def __init__(self):
        super().__init__()

        self.title("Quiz Wiedzy")
        self.geometry("600x400")
        self.configure(bg="#f4f4f4")

        # Add in StartScreen class
        player_name_label = ttk.Label(self, text="Podaj swoje imię:", font=("Arial", 14))
        player_name_label.pack(pady=10)

        self.player_name_entry = ttk.Entry(self)
        self.player_name_entry.pack(pady=5)
        self.player_name_entry.insert(0, "Gracz")  # Default value

        self.create_widgets()

    def create_widgets(self):
        title_label = ttk.Label(self, text="Quiz Wiedzy", font=("Arial", 24, "bold"))
        title_label.pack(side="top", pady=10)

        # dropdown for category selection
        categories = ["Historia", "Nauka", "Kultura", "Losowy"]
        self.selected_category = tk.StringVar(value=categories[0])

        category_label = ttk.Label(self, text="Wybierz kategorię:", font=("Arial", 14))
        category_label.pack(pady=10)

        category_dropdown = ttk.Combobox(self, values=categories, textvariable=self.selected_category)
        category_dropdown.pack(pady=5)

        start_button = ttk.Button(self, text="Rozpocznij Quiz", command=self.start_quiz)
        start_button.pack(pady=10)

        exit_button = ttk.Button(self, text="Wyjdź", command=self.quit)
        exit_button.pack(pady=10)

    def start_quiz(self):
        # print("Start quiz - Tu w przyszłości uruchomimy kolejny widok!")
        chosen_category = self.selected_category.get()  
        player_name = self.player_name_entry.get()    
        questions = load_questions(chosen_category)
        print(f"Wybrana kategoria: {chosen_category}")

        if questions:
            QuizScreen(self, questions, player_name)
        else:
            print("Brak pytań dla tej kategorii.")



if __name__ == "__main__":
    app = StartScreen()
    app.mainloop()