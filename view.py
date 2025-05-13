# quiz_app/view.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class QuizView:

    def __init__(self, root, controller):
        self.root = root  # Główne okno aplikacji
        self.controller = controller  # Odniesienie do kontrolera
        self.root.title("Quiz Wiedzy")
        self.root.geometry("750x650")

        self.current_frame = None 
        self._timer_label = None   
        self._timer_id = None   
        self.current_question_object = None  

        self._setup_styles()  
        self.show_start_screen()  # Wyświetlenie ekranu startowego

    def _setup_styles(self):
        """
        Konfiguracja stylow.
        """
        self.style = ttk.Style()
        
        self.style.theme_use('clam')

        # style
    
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure(
            "TLabel", background="#f0f0f0", font=("Arial", 12))
        self.style.configure("Title.TLabel", background="#f0f0f0", font=(
            "Arial", 22, "bold"), foreground="#333333")
        self.style.configure("Category.TLabel", background="#f0f0f0", font=(
            "Arial", 14, "bold"), foreground="#444444")
        self.style.configure("Question.TLabel", background="#f0f0f0", font=(
            "Arial", 16, "bold"), wraplength=680, foreground="#222222", justify=tk.CENTER)
        self.style.configure("Answer.TButton", font=(
            "Arial", 13), padding=12, width=45, background="#e0e0e0", relief="flat")
        self.style.map("Answer.TButton",
                       background=[('active', '#c0c0c0'),
                                   ('disabled', '#d9d9d9')],
                       foreground=[('disabled', '#a0a0a0')])
        self.style.configure("Correct.Answer.TButton", font=(
            "Arial", 13), padding=12, width=45)
        self.style.configure("Wrong.Answer.TButton", font=(
            "Arial", 13), padding=12, width=45)
        self.style.map("Correct.Answer.TButton", background=[
                       ('!disabled', '#90ee90')])  # Jasnozielony
        self.style.map("Wrong.Answer.TButton", background=[
                       ('!disabled', '#f08080')])   # Jasnoczerwony
        self.style.configure("Control.TButton", font=(
            "Arial", 13, "bold"), padding=10, foreground="white", background="#007bff")
        self.style.map("Control.TButton", background=[('active', '#0056b3')])
        self.style.configure("Timer.TLabel", background="#f0f0f0", font=(
            "Arial", 20, "bold"), foreground="red")
        self.style.configure("Result.TLabel", background="#f0f0f0", font=(
            "Arial", 15), foreground="#333333")
        self.style.configure(
            "Feedback.TLabel", background="#f0f0f0", font=("Arial", 14, "italic"))
        self.style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        self.style.configure("Treeview", rowheight=25, font=("Arial", 11))

    def _clear_frame(self):

        if self._timer_id:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None
        if self.current_frame:
            for widget in self.current_frame.winfo_children():
                widget.destroy()
            self.current_frame.destroy()
        self.current_frame = ttk.Frame(
            self.root, padding="25 25 25 25", style="TFrame")
        self.current_frame.pack(expand=True, fill=tk.BOTH)

    def show_start_screen(self):
        """
        ekran startowy quizu.
        """
        self._clear_frame()
        ttk.Label(self.current_frame, text="Witaj w Quizie Wiedzy!",
                  style="Title.TLabel").pack(pady=(15, 30))

        # okno dla imię gracza
        name_frame = ttk.Frame(self.current_frame, style="TFrame")
        name_frame.pack(pady=10)
        ttk.Label(name_frame, text="Podaj swoje imię:", font=(
            "Arial", 13)).pack(side=tk.LEFT, padx=(0, 10))
        self.player_name_entry = ttk.Entry(
            name_frame, font=("Arial", 13), width=35)
        self.player_name_entry.pack(side=tk.LEFT)
        self.player_name_entry.focus()  # Ustawienie fokusu na polu imienia

        # Okienko na wybór kategorii
        category_frame = ttk.Frame(self.current_frame, style="TFrame")
        category_frame.pack(pady=20)
        ttk.Label(category_frame, text="Wybierz kategorię:",
                  style="Category.TLabel").pack(side=tk.LEFT, padx=(0, 10))
        categories = ["Wszystkie"] + self.controller.get_categories()
        self.category_var = tk.StringVar(self.root)

        
        if categories and categories != ["Wszystkie"]:
            self.category_var.set(categories[0])
            category_menu = ttk.OptionMenu(
                category_frame, self.category_var, categories[0], *categories)
        
        else:
            self.category_var.set("Brak kategorii")
            category_menu = ttk.OptionMenu(
                category_frame, self.category_var, "Brak kategorii")
            category_menu.config(state=tk.DISABLED)

        category_menu.config(width=25)
        category_menu.pack(side=tk.LEFT)

        # Okienko na limit czasu
        time_limit_frame = ttk.Frame(self.current_frame, style="TFrame")
        time_limit_frame.pack(pady=10)
        ttk.Label(time_limit_frame, text="Limit czasu na pytanie (sekundy, 0 = bez limitu):", font=(
            "Arial", 13)).pack(side=tk.LEFT, padx=(0, 10))
        self.time_limit_entry = ttk.Entry(
            time_limit_frame, font=("Arial", 13), width=10)
        self.time_limit_entry.insert(0, "15") #moze byc zmieniony
        self.time_limit_entry.pack(side=tk.LEFT)

        start_button = ttk.Button(self.current_frame, text="Rozpocznij Quiz",
                                  command=self.controller.start_quiz, style="Control.TButton")
        start_button.pack(pady=30)

        results_button = ttk.Button(self.current_frame, text="Historia Wyników",
                                    command=self.controller.show_results_history, style="Control.TButton")
        results_button.pack(pady=15)

 
        if self.category_var.get() == "Brak kategorii":
            start_button.config(state=tk.DISABLED)

    def show_question_screen(self, question, question_number, total_questions, time_limit):
        """
        Wyświetla ekran z pytaniem.
        """
        self._clear_frame()
        self.current_question_object = question

        # Ramka na postęp i timer
        top_info_frame = ttk.Frame(self.current_frame, style="TFrame")
        top_info_frame.pack(fill=tk.X, pady=(0, 20))

        progress_text = f"Pytanie {question_number} z {total_questions}"
        ttk.Label(top_info_frame, text=progress_text, font=(
            "Arial", 12, "italic")).pack(side=tk.LEFT, padx=10)

        if time_limit > 0:
            self._timer_label = ttk.Label(
                top_info_frame, text=f"Czas: {time_limit}", style="Timer.TLabel")
            self._timer_label.pack(side=tk.RIGHT, padx=10)
            self._start_timer(time_limit)

        ttk.Label(self.current_frame, text=question.text,
                  style="Question.TLabel").pack(pady=(10, 30))

        self.answer_buttons = []
        answers_frame = ttk.Frame(self.current_frame, style="TFrame")
        answers_frame.pack(pady=15)

        # Tworzenie przycisków odpowiedzi
        for i, answer_text in enumerate(question.answers):
            btn = ttk.Button(answers_frame, text=f"{chr(65+i)}. {answer_text}",
                             command=lambda idx=i: self._handle_answer_selection(
                                 idx),
                             style="Answer.TButton")
            btn.pack(pady=7, fill=tk.X, padx=20)
            self.answer_buttons.append(btn)

        self.feedback_label = ttk.Label(
            self.current_frame, text="", style="Feedback.TLabel")
        self.feedback_label.pack(pady=20)

        self.next_question_button = ttk.Button(self.current_frame, text="Następne pytanie",
                                               command=self.controller.next_question,
                                               state=tk.DISABLED, style="Control.TButton")
        self.next_question_button.pack(pady=25)

    def _start_timer(self, remaining_time):

        if self._timer_id:  
            self.root.after_cancel(self._timer_id)

        if remaining_time >= 0 and self._timer_label:
            self._timer_label.config(text=f"Czas: {remaining_time}")
        
            self._timer_id = self.root.after(
                1000, lambda: self._start_timer(remaining_time - 1))
        elif remaining_time < 0 and self._timer_label:  # Czas minął
            self._timer_label.config(text="Czas minął!")
            self.controller.time_up()  

    def _handle_answer_selection(self, selected_index):

        if self._timer_id:  # Zatrzymanie timeru po udzieleniu odpowiedzi
            self.root.after_cancel(self._timer_id)
            self._timer_id = None

        is_correct = self.controller.submit_answer(
            self.current_question_object, selected_index)
        self.show_feedback(is_correct, selected_index,
                           self.current_question_object.correct_answer_index)
        
        self.next_question_button.config(state=tk.NORMAL)
        for btn in self.answer_buttons:
            btn.config(state=tk.DISABLED)  # Wyłączenie przyciskow odpowiedzi

    def show_feedback(self, is_correct, selected_idx, correct_idx):

        correct_answer_char = chr(
            65 + correct_idx)  # Litera poprawnej odpowiedzi (A, B, C, D)
        if selected_idx == -1:  # Timeout
            self.feedback_label.config(
                text=f"Czas minął! Poprawna odpowiedź: {correct_answer_char}. {self.current_question_object.answers[correct_idx]}", foreground="orange", font=("Arial", 14, "italic"))
        elif is_correct:
            self.feedback_label.config(text="Poprawna odpowiedź!", foreground="green", font=(
                "Arial", 14, "italic", "bold"))
            if 0 <= selected_idx < len(self.answer_buttons):
                self.answer_buttons[selected_idx].config(
                    style="Correct.Answer.TButton")
        else:
            self.feedback_label.config(
                text=f"Błędna odpowiedź. Poprawna to: {correct_answer_char}. {self.current_question_object.answers[correct_idx]}", foreground="red", font=("Arial", 14, "italic"))
            if 0 <= selected_idx < len(self.answer_buttons):
                self.answer_buttons[selected_idx].config(
                    style="Wrong.Answer.TButton")

            # Podświetlenie poprawnej odpowiedzi
        if 0 <= correct_idx < len(self.answer_buttons):
            self.answer_buttons[correct_idx].config(
                style="Correct.Answer.TButton")

    def show_final_score_screen(self, results):
        """
        Wyświetla ekran końcowy z podsumowaniem wyników quizu.
    
        """
        self._clear_frame()
        ttk.Label(self.current_frame, text="Koniec Quizu!",
                  style="Title.TLabel").pack(pady=25)
        ttk.Label(self.current_frame,
                  text=f"Twój wynik: {results['score']}/{results['total_questions']}", style="Result.TLabel").pack(pady=7)
        ttk.Label(self.current_frame,
                  text=f"Procent poprawnych odpowiedzi: {results['percentage']}%", style="Result.TLabel").pack(pady=7)
        ttk.Label(self.current_frame,
                  text=f"Czas trwania quizu: {results['duration_seconds']} sekund", style="Result.TLabel").pack(pady=7)
        ttk.Label(self.current_frame, text=results['comment'], font=("Arial", 17, "italic", "bold"), foreground="#006400" if results['percentage'] >= 75 else (
            "#DAA520" if results['percentage'] >= 50 else "#8B0000")).pack(pady=20)

        self.final_feedback_label = ttk.Label(
            self.current_frame, text="", style="Feedback.TLabel")
        self.final_feedback_label.pack(pady=10)

        save_button = ttk.Button(self.current_frame, text="Zapisz wynik",
                                 command=self.controller.save_score, style="Control.TButton")
        save_button.pack(pady=15)

        # Ramka na przyciski 
        buttons_frame = ttk.Frame(self.current_frame, style="TFrame")
        buttons_frame.pack(pady=15)

        play_again_button = ttk.Button(buttons_frame, text="Zagraj ponownie",
                                       command=self.show_start_screen, style="Control.TButton")
        play_again_button.pack(side=tk.LEFT, padx=12)

        results_history_button = ttk.Button(buttons_frame, text="Historia Wyników",
                                            command=self.controller.show_results_history, style="Control.TButton")
        results_history_button.pack(side=tk.LEFT, padx=12)

        exit_button = ttk.Button(buttons_frame, text="Zakończ",
                                 command=self.root.quit, style="Control.TButton")
        exit_button.pack(side=tk.LEFT, padx=12)

    def show_results_history_screen(self, history_data):

        self._clear_frame()
        ttk.Label(self.current_frame, text="Historia Wyników",
                  style="Title.TLabel").pack(pady=25)

        if not history_data:
            ttk.Label(self.current_frame, text="Brak zapisanych wyników.",
                      style="Result.TLabel").pack(pady=15)
        else:
            cols = ("Imię gracza", "Data", "Wynik",
                    "Procent (%)", "Czas quizu (s)")
        
            tree_container = ttk.Frame(self.current_frame, style="TFrame")
            tree_container.pack(expand=True, fill=tk.BOTH, pady=10, padx=10)

            tree = ttk.Treeview(tree_container, columns=cols,
                                show='headings', style="Treeview")
            for col_name in cols:
                tree.heading(col_name, text=col_name, anchor=tk.W)
                # Ustawienie szerokości kolumn
                if col_name == "Imię gracza":
                    tree.column(col_name, width=150,
                                minwidth=100, stretch=tk.NO)
                elif col_name == "Data":
                    tree.column(col_name, width=160,
                                minwidth=120, stretch=tk.NO)
                elif col_name == "Wynik":
                    tree.column(col_name, width=80, minwidth=60,
                                anchor=tk.CENTER, stretch=tk.NO)
                elif col_name == "Procent (%)":
                    tree.column(col_name, width=100, minwidth=80,
                                anchor=tk.CENTER, stretch=tk.NO)
                elif col_name == "Czas quizu (s)":
                    tree.column(col_name, width=120, minwidth=100,
                                anchor=tk.CENTER, stretch=tk.NO)

            for row in history_data:
                tree.insert("", tk.END, values=row)

            # Scrollbary
            scrollbar_y = ttk.Scrollbar(
                tree_container, orient=tk.VERTICAL, command=tree.yview)
            scrollbar_x = ttk.Scrollbar(
                tree_container, orient=tk.HORIZONTAL, command=tree.xview)
            tree.configure(yscrollcommand=scrollbar_y.set,
                           xscrollcommand=scrollbar_x.set)

            
            tree_container.grid_rowconfigure(0, weight=1)
            tree_container.grid_columnconfigure(0, weight=1)

            tree.grid(row=0, column=0, sticky='nsew')
            scrollbar_y.grid(row=0, column=1, sticky='ns')
            scrollbar_x.grid(row=1, column=0, sticky='ew')

        back_button = ttk.Button(self.current_frame, text="Wróć do Menu Głównego",
                                 command=self.show_start_screen, style="Control.TButton")
        back_button.pack(pady=25)

    def get_player_name(self):

        name = self.player_name_entry.get()
        if not name.strip():  
            messagebox.showwarning(
                "Brak imienia", "Proszę podać imię gracza.", parent=self.root)
            return None
        return name.strip()

    def get_selected_category(self):

        selected = self.category_var.get()
        if selected == "Brak kategorii":  
            return None
        return selected

    def get_time_limit(self):

        try:
            limit_str = self.time_limit_entry.get()
            if not limit_str.strip(): 
                return 0
            limit = int(limit_str)
            if limit < 0:
                messagebox.showwarning(
                    "Nieprawidłowy czas", "Limit czasu nie może być ujemny. Ustawiono domyślny (15s).", parent=self.root)
                self.time_limit_entry.delete(0, tk.END)
                self.time_limit_entry.insert(0, "15")
                return 15  
            return limit
        except ValueError:
            messagebox.showwarning(
                "Nieprawidłowy format czasu", "Proszę wprowadzić liczbę całkowitą jako limit czasu. Ustawiono domyślny (15s).", parent=self.root)
            self.time_limit_entry.delete(0, tk.END)
            self.time_limit_entry.insert(0, "15")
            return 15  

    def show_message(self, title, message, type="info"):

        if type == "error":
            messagebox.showerror(title, message, parent=self.root)
        elif type == "warning":
            messagebox.showwarning(title, message, parent=self.root)
        else:
            messagebox.showinfo(title, message, parent=self.root)

    def update_final_score_feedback(self, message, color="blue"):

        if hasattr(self, 'final_feedback_label') and self.final_feedback_label:
            self.final_feedback_label.config(text=message, foreground=color)
