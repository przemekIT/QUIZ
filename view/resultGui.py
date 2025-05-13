import tkinter as tk
from tkinter import ttk
import time
import os
import csv

class ResultView(tk.Frame): 
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.pack()

    def display_result(self):
        self.time_elapsed = round(time.time() - self.controller.start_time, 2)

        score = self.controller.quiz.correct_count
        total_questions = self.controller.quiz.total_questions()

        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Quiz Completed!", font=("Arial", 24)).pack(pady=20)
        tk.Label(self, text=f"Score: {score}/{total_questions}", font=("Arial", 18)).pack(pady=10)

        comment = "Świetnie!" if score / total_questions >= 0.8 else "Spróbuj ponownie!"
        tk.Label(self, text=comment, font=("Arial", 14)).pack(pady=5)

        tk.Label(self, text="Imię:", font=("Arial", 12)).pack(pady=(20, 5))
        self.name_entry = tk.Entry(self, font=("Arial", 12), width=30)
        self.name_entry.pack()

        tk.Button(self, text="Zapisz wynik", font=("Arial", 12), command=self.save_result).pack(pady=10)

        tk.Button(self, text="Pokaż wyniki", font=("Arial", 12), command=self.show_results_table).pack(pady=10)

        tk.Button(self, text="Restart", font=("Arial", 12), command=self.controller.show_start_view).pack(pady=10)

    def save_result(self):
        player_name = self.name_entry.get().strip()
        if not player_name:
            self.show_message("❗ Podaj imię przed zapisem.")
            return

        self.controller.save_result(player_name, self.time_elapsed)
        self.show_message("✅ Wynik zapisany!")

    def show_message(self, message):
        if hasattr(self, 'msg_label'):
            self.msg_label.config(text=message)
        else:
            self.msg_label = tk.Label(self, text=message, font=("Arial", 12), fg='green')
            self.msg_label.pack(pady=5)

    def show_results_table(self):
        filepath = "assets/save/results.csv"
        if not os.path.exists(filepath):
            self.show_message("❗ Plik z wynikami nie istnieje.")
            return

        if hasattr(self, 'results_tree'):
            self.results_tree.destroy()

        self.results_tree = ttk.Treeview(self, columns=("Imię", "Data", "Wynik", "Czas"), show='headings')
        self.results_tree.heading("Imię", text="Imię")
        self.results_tree.heading("Data", text="Data")
        self.results_tree.heading("Wynik", text="Wynik")
        self.results_tree.heading("Czas", text="Czas")

        self.results_tree.pack(pady=10)

        try:
            with open(filepath, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row:
                        self.results_tree.insert("", tk.END, values=row)
        except Exception as e:
            self.show_message(f"❗ Błąd przy czytaniu wyników: {e}")
