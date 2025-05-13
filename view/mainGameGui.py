import tkinter as tk

class StartView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg='#f0f0f0')  # Світлий фон
        self.controller = controller
        self.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Стиль заголовка
        title_label = tk.Label(
            self,
            text="Quiz Wiedzy",
            font=("Arial", 32, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(pady=40)

        # Інструкція
        info_label = tk.Label(
            self,
            text="Wybierz kategorię, aby rozpocząć quiz:",
            font=("Arial", 16),
            bg='#f0f0f0',
            fg='#555555'
        )
        info_label.pack(pady=10)

        # Генеруємо кнопки для кожної категорії
        for category in self.controller.categories:
            btn = tk.Button(
                self,
                text=category,
                font=("Arial", 14),
                width=20,
                bg='#4CAF50',
                fg='white',
                activebackground='#45a049',
                command=lambda c=category: self.controller.start_quiz(c)
            )
            btn.pack(pady=5)


