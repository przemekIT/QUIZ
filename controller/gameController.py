import tkinter as tk
import time
from model.dataLoad import DataLoader
from model.quize import Quiz
from view.mainGameGui import StartView
from view.questionGui import QuestionView
from view.resultGui import ResultView

class QuizController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quiz Wiedzy")
        self.root.geometry("600x800")
        self.root.configure(bg='#f0f0f0')

        self.data, self.categories = DataLoader.load_questions_from_folder("assets/tests")

        self.quiz = None
        self.start_time = None

        self.start_view = StartView(self.root, self)
        self.question_view = QuestionView(self.root, self)
        self.result_view = ResultView(self.root, self)

        self.show_start_view()

    def show_start_view(self):
        self.start_view.pack()
        self.question_view.pack_forget()
        self.result_view.pack_forget()

    def start_quiz(self, category):
        questions = self.data[category]
        self.quiz = Quiz(questions) 
        self.start_time = time.time() 
        self.show_question_view()

    def show_question_view(self):
        self.start_view.pack_forget()
        self.question_view.pack()
        self.result_view.pack_forget()
        self.question_view.display_question()

    def process_answer(self, answer):
        self.question_view.stop_timer()
        correct = self.quiz.answer_current(answer)
        self.question_view.show_feedback(correct)

    def next_question(self):
        if self.quiz.is_finished():
            self.show_result_view()
        else:
            self.question_view.display_question()

    def show_result_view(self):
        self.start_view.pack_forget()
        self.question_view.pack_forget()
        self.result_view.pack()
        self.time_elapsed = time.time() - self.start_time
        self.result_view.display_result()
        

    def save_result(self, name, time_elapsed):
        DataLoader.save_result("assets/save/results.csv", name, self.quiz.correct_count, self.quiz.total_questions(), time_elapsed)

    def run(self):
        self.root.mainloop()