import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import random
import os
import csv

class QuizController:
    MAX_QUESTIONS = 12

    def __init__(self):
        from view.quiz_gui import QuizGUI
        self.player_name = ""
        self.player_age = 0
        self.total_points = 0
        self.total_questions = 0
        self.total_time = 0

        self.questions_cache = {1: [], 2: [], 3: []}
        self.gui = QuizGUI(self)

    def ask_name(self):
        self.gui.show_name_input()

    def save_name(self, name):
        self.player_name = name

    def save_age(self, age):
        self.player_age = age
        self.show_player_dashboard()

    def show_player_dashboard(self):
        self.gui.show_player_dashboard()

    def select_question(self, points):
        if not self.questions_cache[points]:
            filename = os.path.join("data", f"questions_{points}.json")
            if os.path.exists(filename):
                with open(filename, encoding="utf-8") as f:
                    self.questions_cache[points] = json.load(f)
            else:
                messagebox.showerror("Błąd", f"Brak pliku z pytaniami: {filename}")
                return

        question_data = random.choice(self.questions_cache[points])
        self.questions_cache[points].remove(question_data)
        self.gui.show_question(question_data)

    def check_answer(self, choice, question_data):
        print(">>> Sprawdzam odpowiedź")
        self.total_questions += 1
        if choice and choice == question_data.get("poprawna"):
            self.total_points += question_data.get("punkty", 0)
            messagebox.showinfo("Poprawna odpowiedź", "Brawo! Zdobywasz punkty!")
        else:
            poprawna_odp = question_data.get("poprawna", "X")
            tresc = question_data.get("odpowiedzi", {}).get(poprawna_odp, "Brak danych")
            messagebox.showwarning("Błędna odpowiedź", f"Poprawna odpowiedź to: {poprawna_odp}: {tresc}")

        if self.total_questions >= self.MAX_QUESTIONS:
            print(">>> Maksymalna liczba pytań — zapisuję wyniki")
            self.save_results_to_csv()
            messagebox.showinfo("Koniec gry", f"Gratulacje {self.player_name}!\nPunkty: {self.total_points}")
        else:
            self.show_player_dashboard()

    def get_average_time(self):
        if self.total_questions == 0:
            return 0.0
        return self.total_time / self.total_questions

    def show_ranking(self):
        pass

    def save_results_to_csv(self):
        print(">>> ZAPIS DO PLIKU CSV")
        filename = "wyniki.csv"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = ["Data", "Imię", "Wiek", "Punkty", "Liczba pytań"]
        row = [now, self.player_name, self.player_age, self.total_points, self.total_questions]

        file_exists = os.path.exists(filename)
        try:
            with open(filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(header)
                writer.writerow(row)
            print(">>> ZAPISANO:", row)
        except Exception as e:
            print(">>> BŁĄD ZAPISU DO CSV:", e)

    def run(self):
        self.gui.show_start_screen()
        self.gui.run()


if __name__ == "__main__":
    app = QuizController()
    app.run()
