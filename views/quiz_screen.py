import tkinter as tk
from tkinter import ttk
from models.result_savers import save_result
from models.quiz_game import QuizGame

class QuizScreen(tk.Toplevel):
    def __init__(self, parent, questions, player_name, chosen_category):
        super().__init__(parent)

        self.title("Quiz Wiedzy")
        self.geometry("600x400")
        self.configure(bg="#f4f4f4")

        self.quiz_game = QuizGame(questions) # Initialize QuizGame instance

        self.player_name = player_name
        self.category = chosen_category

        # Timer label
       
        self.time_label = ttk.Label(self, text=f"Czas: {self.quiz_game.time_left}s", font=("Arial", 14))
        self.time_label.pack(pady=10)

        self.create_widgets()
        self.load_question()

        # Start the timer for the first question! 
        self.quiz_game.start_timer(lambda t: self.time_label.config(text=f"Czas {t}s"), self.disable_answer_buttons, self.show_next_button)

    def create_widgets(self):
        """Creates quiz UI elements."""
        self.title_label = ttk.Label(self, text="Quiz Wiedzy", font=("Arial", 24, "bold"))
        self.title_label.pack(side="top", pady=10)

        self.question_label = ttk.Label(self, text="", font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.answer_buttons = []
        for _ in range(4):
            btn = ttk.Button(self, text="", command=lambda a="": self.check_answer(a))
            btn.pack(pady=5)
            self.answer_buttons.append(btn)

        self.feedback_label = ttk.Label(self, text="", font=("Arial", 12, "bold"))
        self.feedback_label.pack(pady=10)

        self.next_button = ttk.Button(self, text="Następne pytanie", command=self.next_question)
        self.next_button.pack(pady=10)
        self.next_button.pack_forget()

    def load_question(self):
        """Loads the next question or ends the quiz."""
        question_data = self.quiz_game.get_current_question()

        if question_data:
            self.question_label.config(text=question_data["question"])

            for i, answer in enumerate(question_data["answers"]):
                self.answer_buttons[i].config(text=answer, command=lambda a=answer: self.check_answer(a))
                self.answer_buttons[i].config(state="normal") # Enable the buttons, to be able to answer the next question 

            self.feedback_label.config(text="")  
            self.next_button.pack_forget()

        else:
            self.end_quiz()

    def check_answer(self, selected_answer):
        """Checks the answer."""

        # Stop the timer 
        self.quiz_game.stop_timer()

        # Disable all answer buttons after clicking one 
        for btn in self.answer_buttons:
            btn.config(state="disabled")
        
        is_correct = self.quiz_game.check_answer(selected_answer)
        # correct_answer = self.questions[self.current_question_index]["correct_answer"]
        # if selected_answer == correct_answer:
        if is_correct:
            self.feedback_label.config(text="✅ Poprawna odpowiedź!", foreground="green")           
        else:
            self.feedback_label.config(text="❌ Niepoprawna odpowiedź!", foreground="red")
            
        self.next_button.pack()

    def next_question(self):
        """Moves to the next question and resests the timer."""
        if self.quiz_game.next_question():
            self.load_question()

            # Reset the timer  
            self.quiz_game.reset_timer()           
            self.time_label.config(text=f"Czas: {self.quiz_game.time_left}s")            

            # Start the timer and pass a function to disable the buttons when time's up
            self.quiz_game.start_timer(
                lambda t: self.time_label.config(text=f"Czas: {t}s"),
                self.disable_answer_buttons, 
                self.show_next_button
            )
        else:
            self.end_quiz()

    def disable_answer_buttons(self):
        """Disables all answer buttons when time runs out."""
        for btn in self.answer_buttons:
            btn.config(state="disabled")

    def show_next_button(self):
        """Makes the 'Next Question' button visible when timer ends. """
        self.next_button.pack()

    def end_quiz(self):
        """Ends the quiz and saves the result."""
        final_score = self.quiz_game.get_score()
        total_questions = len(self.quiz_game.questions)

        self.question_label.config(text=f"Quiz zakończony! Wynik: {final_score}/{total_questions}")

        for btn in self.answer_buttons:
            btn.pack_forget()
        self.next_button.pack_forget()

        # Save result
        save_result(self.player_name, final_score, len(self.quiz_game.questions), 0, self.category)  # No timer, so total time is omitted

        self.feedback_label.config(text=f"📜 Wynik zapisano dla: {self.player_name}!", foreground="blue")