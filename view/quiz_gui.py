import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, date

class QuizGUI:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Quiz App")
        self.root.geometry("600x400")
        self.root.configure(bg="#cce6ff")
        self.current_frame = None
        self.timer_label = None
        self.remaining_seconds = 0

        self.button_style = {
            "bg": "#001F3F",
            "fg": "white",
            "activebackground": "#004080",
            "font": ("Helvetica", 11, "bold"),
            "bd": 3,
            "relief": "ridge",
            "padx": 10,
            "pady": 5
        }

    def show_start_screen(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg="#cce6ff")

        tk.Label(frame, text="Witaj w Quizie!", font=('Helvetica', 18), bg="#cce6ff").pack(pady=20)
        tk.Button(frame, text="START", command=self.controller.ask_name, **self.button_style).pack(pady=10)
        

        frame.pack(expand=True)
        self.current_frame = frame

    def show_name_input(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg="#cce6ff")

        tk.Label(frame, text="Podaj imię:", bg="#cce6ff").pack(pady=(10, 0))
        name_entry = tk.Entry(frame)
        name_entry.pack(pady=(0, 10))

        tk.Label(frame, text="Wybierz datę urodzenia:", bg="#cce6ff").pack()
        date_frame = tk.Frame(frame, bg="#cce6ff")

        days = [str(i) for i in range(1, 32)]
        months = [str(i) for i in range(1, 13)]
        years = [str(i) for i in range(1950, datetime.now().year + 1)]

        day_cb = ttk.Combobox(date_frame, values=days, width=5)
        month_cb = ttk.Combobox(date_frame, values=months, width=5)
        year_cb = ttk.Combobox(date_frame, values=years, width=7)

        day_cb.set("1")
        month_cb.set("1")
        year_cb.set("2000")

        day_cb.pack(side="left", padx=5)
        month_cb.pack(side="left", padx=5)
        year_cb.pack(side="left", padx=5)
        date_frame.pack(pady=(0, 10))

        def save_all():
            name = name_entry.get()
            try:
                birth_day = int(day_cb.get())
                birth_month = int(month_cb.get())
                birth_year = int(year_cb.get())
                birth_date = date(birth_year, birth_month, birth_day)
                today = date.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            except Exception:
                messagebox.showerror("Błąd", "Niepoprawna data urodzenia")
                return

            self.controller.save_name(name)
            self.controller.save_age(age)

        tk.Button(frame, text="Dalej", command=save_all, **self.button_style).pack()
        

        frame.pack(expand=True)
        self.current_frame = frame

    def show_player_dashboard(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg="#cce6ff")

        tk.Label(frame, text=datetime.now().strftime("%Y-%m-%d %H:%M"), anchor="e", bg="#cce6ff").pack(anchor="ne", padx=10, pady=5)
        tk.Label(frame, text=f"Witaj, {self.controller.player_name}!", font=('Helvetica', 16), bg="#cce6ff").pack(pady=5)
        tk.Label(frame, text=f"Wiek: {self.controller.player_age}", bg="#cce6ff").pack()
        tk.Label(frame, text=f"Liczba pytań: {self.controller.total_questions}", bg="#cce6ff").pack()
        tk.Label(frame, text=f"Punkty: {self.controller.total_points}", bg="#cce6ff").pack()
        tk.Label(frame, text=f"Średni czas: {self.controller.get_average_time():.1f}s", bg="#cce6ff").pack(pady=5)

        choice_frame = tk.Frame(frame, bg="#cce6ff")
        tk.Label(choice_frame, text="Wybierz poziom pytania:", font=('Helvetica', 14), bg="#cce6ff").pack(side="top", pady=10)
        tk.Button(choice_frame, text="1 punkt", width=12, command=lambda: self.controller.select_question(1), **self.button_style).pack(side="left", padx=5)
        tk.Button(choice_frame, text="2 punkty", width=12, command=lambda: self.controller.select_question(2), **self.button_style).pack(side="left", padx=5)
        tk.Button(choice_frame, text="3 punkty", width=12, command=lambda: self.controller.select_question(3), **self.button_style).pack(side="left", padx=5)
        choice_frame.pack(pady=15)

        frame.pack(expand=True, fill="both")
        self.current_frame = frame

    def show_question(self, question_data):
        self.clear_frame()
        self.remaining_seconds = 30
        self.start_time = datetime.now()

        frame = tk.Frame(self.root, bg="#cce6ff")

        top_bar = tk.Frame(frame, bg="#cce6ff")
        tk.Label(top_bar, text=datetime.now().strftime("%Y-%m-%d %H:%M"), anchor="e", bg="#cce6ff").pack(side="right", padx=10)
        self.timer_label = tk.Label(top_bar, text=f"Czas: {self.remaining_seconds}s", font=('Helvetica', 12), bg="#cce6ff")
        self.timer_label.pack(side="left", padx=10)
        top_bar.pack(anchor="ne", fill="x")

        self.update_timer()

        tk.Label(frame, text=question_data["pytanie"], font=('Helvetica', 14), wraplength=500, bg="#cce6ff").pack(pady=10)

        button_frame_top = tk.Frame(frame, bg="#cce6ff")
        button_frame_bottom = tk.Frame(frame, bg="#cce6ff")

        tk.Button(button_frame_top, text=f"A: {question_data['odpowiedzi']['A']}", width=25,
                  command=lambda: self.controller.check_answer('A', question_data), **self.button_style).pack(side="left", padx=5, pady=5)
        tk.Button(button_frame_top, text=f"B: {question_data['odpowiedzi']['B']}", width=25,
                  command=lambda: self.controller.check_answer('B', question_data), **self.button_style).pack(side="left", padx=5, pady=5)

        tk.Button(button_frame_bottom, text=f"C: {question_data['odpowiedzi']['C']}", width=25,
                  command=lambda: self.controller.check_answer('C', question_data), **self.button_style).pack(side="left", padx=5, pady=5)
        tk.Button(button_frame_bottom, text=f"D: {question_data['odpowiedzi']['D']}", width=25,
                  command=lambda: self.controller.check_answer('D', question_data), **self.button_style).pack(side="left", padx=5, pady=5)

        button_frame_top.pack(pady=(10, 5))
        button_frame_bottom.pack(pady=(0, 10))
        frame.pack(expand=True, fill="both")
        self.current_frame = frame

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def update_timer(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            if self.timer_label.winfo_exists():
                self.timer_label.config(text=f"Czas: {self.remaining_seconds}s")

                self.root.after(1000, self.update_timer)
        else:
            messagebox.showwarning("Czas minął", "Nie zdążyłeś odpowiedzieć!")
            self.controller.check_answer("", {"poprawna": "X"})

    def run(self):
        self.root.mainloop()