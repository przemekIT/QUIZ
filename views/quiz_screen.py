import tkinter as tk
from tkinter import ttk
from models.result_savers import save_result


class QuizScreen(tk.Toplevel):
    def __init__(self, parent, questions, player_name):
        super().__init__(parent)

        self.title("Quiz Wiedzy")
        self.geometry("600x400")
        self.configure(bg="#f4f4f4")

        self.questions = questions  # Store all questions
        self.player_name = player_name 

        self.score = 0

        self.current_question_index = 0  # Track which question is displayed
        self.time_limit = 15 # seconds

        self.create_widgets()

    def create_widgets(self):

        self.title_label = ttk.Label(self, text="Quiz Wiedzy", font=("Arial", 24, "bold"))
        self.title_label.pack(side="top", pady=10)

        self.question_label = ttk.Label(self, text="", font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.answer_buttons = []
        for _ in range(4):
            btn = ttk.Button(self, text="", command=lambda a="": self.check_answer(a))
            btn.pack(pady=5)
            self.answer_buttons.append(btn)

        # Timer label

        self.timer_label = ttk.Label(self, text=f"Czas: {self.time_limit}", font=("Arial", 12))
        self.timer_label.pack(pady=10)

        self.feedback_label = ttk.Label(self, text="", font=("Arial", 12, "bold"))
        self.feedback_label.pack(pady=10)

        self.next_button = ttk.Button(self, text="Następne pytanie", command=self.next_question)
        self.next_button.pack(pady=10)
        self.next_button.pack_forget()  # Hide at start

        self.load_question()

    def load_question(self):
        """Load the next question if available, else end quiz."""
        if self.current_question_index < len(self.questions):
            self.remainining_time = self.time_limit

            question_data = self.questions[self.current_question_index]
            self.question_label.config(text=question_data["question"])

            for i, answer in enumerate(question_data["answers"]):
                self.answer_buttons[i].config(text=answer, command=lambda a=answer: self.check_answer(a))

            self.feedback_label.config(text="")  # Reset feedback
            self.next_button.pack_forget()  # Hide "Next" button

            self.update_timer()  # Start countdown

        else:
            self.end_quiz()

    def update_timer(self):
        """Update the timer label every second"""
        if self.remainining_time > 0:
            self.timer_label.config(text=f"Czas: {self.remainining_time} s")
            self.remainining_time -= 1
            self.after(1000, self.update_timer) # Update every second
        else:
            self.time_up() # handle timeout

    def time_up(self):
        """Handle when time runs out"""
        self.feedback_label.config(text="⏳ Czas minął! ❌", foreground="red")
        self.next_button.pack()  # Show "Next" button

    def check_answer(self, selected_answer):
        correct_answer = self.questions[self.current_question_index]["correct_answer"]
        if selected_answer == correct_answer:
            self.feedback_label.config(text="✅ Poprawna odpowiedź!", foreground="green")
            self.score += 1
        else:
            self.feedback_label.config(text="❌ Niepoprawna odpowiedź!", foreground="red")

        self.next_button.pack()  # Show "Next" button after answering

    def next_question(self):
        """Advance to the next question."""
        self.current_question_index += 1
        self.load_question()

    def end_quiz(self):
        self.question_label.config(text=f"Quiz zakończony! Wynik: {self.score}/{len(self.questions)}")
        for btn in self.answer_buttons:
            btn.pack_forget()
        self.next_button.pack_forget()
        self.timer_label.pack_forget()

        quiz_time = len(self.questions) * self.time_limit  # Approximate total time
        save_result(self.player_name, self.score, len(self.questions), quiz_time)

        self.feedback_label.config(text=f"📜 Wynik zapisano dla: {self.player_name}!", foreground="blue")