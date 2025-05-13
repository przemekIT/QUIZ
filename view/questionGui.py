import tkinter as tk
import random

class QuestionView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg='#f0f0f0')
        self.controller = controller
        self.timer_job = None
        self.time_limit = 15
        self.time_left = self.time_limit
        self.shuffled_options = []

        self.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.timer_label = tk.Label(
            self,
            text="",
            font=("Arial", 14),
            bg='#f0f0f0',
            fg='#333333'
        )
        self.timer_label.pack(pady=10)

        self.question_label = tk.Label(
            self,
            text="",
            wraplength=500,
            justify='center',
            font=("Arial", 18, "bold"),
            bg='#f0f0f0',
            fg='#222222'
        )
        self.question_label.pack(pady=30)

        self.buttons = []
        for i in range(4):
            btn = tk.Button(
                self,
                text="",
                font=("Arial", 14),
                width=40,
                bg='#4CAF50',
                fg='white',
                activebackground='#45a049',
                command=lambda idx=i: self.process_answer(idx)
            )
            btn.pack(pady=8)
            self.buttons.append(btn)

        self.feedback_label = tk.Label(
            self,
            text="",
            font=("Arial", 16),
            bg='#f0f0f0',
            fg='#333333'
        )
        self.feedback_label.pack(pady=20)

        self.next_button = tk.Button(
            self,
            text="Następne pytanie",
            font=("Arial", 14),
            bg='#2196F3',
            fg='white',
            activebackground='#1976D2',
            command=self.controller.next_question
        )
        self.next_button.pack(pady=10)
        self.next_button.config(state='disabled') 
            
    def display_question(self):
        question = self.controller.quiz.questions[self.controller.quiz.current_index]
        self.question_label.config(text=question.text)
        self.feedback_label.config(text="")
        self.next_button.config(state='disabled')

        self.shuffled_options = question.options.copy()
        random.shuffle(self.shuffled_options)

        for i, option in enumerate(self.shuffled_options):
            self.buttons[i].config(text=option, state='normal', bg='#4CAF50')

        self.start_timer()

    def process_answer(self, idx):
        self.stop_timer()

        question = self.controller.quiz.questions[self.controller.quiz.current_index]
        selected_answer_text = self.shuffled_options[idx] 

        correct = (question.correct_answer == selected_answer_text)

        if correct:
            self.feedback_label.config(text="✅ Poprawna odpowiedź!", fg='green')
            self.buttons[idx].config(bg='green')
        else:
            self.feedback_label.config(text="❌ Zła odpowiedź!", fg='red')
            self.buttons[idx].config(bg='red')

        self.disable_buttons()

        self.controller.quiz.answer_current(selected_answer_text)

        self.next_button.config(state='normal')

    def next_question(self):
        if self.controller.quiz.is_finished():
            self.controller.show_result_view() 
        else:
            self.controller.question_view.display_question()
            self.enable_buttons() 
            self.next_button.config(state='disabled') 

    def disable_buttons(self):
        for btn in self.buttons:
            btn.config(state='disabled')

    def start_timer(self):
        self.time_left = self.time_limit
        self.update_timer_label()
        self.timer_job = self.after(1000, self.countdown)

    def countdown(self):
        self.time_left -= 1
        self.update_timer_label()
        if self.time_left <= 0:
            self.feedback_label.config(text="⏰ Czas minął!", fg='red')
            self.disable_buttons()
            self.next_button.config(state='normal')
        else:
            self.timer_job = self.after(1000, self.countdown)

    def update_timer_label(self):
        self.timer_label.config(text=f"Czas: {self.time_left}s")

    def stop_timer(self):
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None
