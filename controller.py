# quiz_app/controller.py

class QuizController:
  

    def __init__(self, model, view_class_ref):
        self.model = model  # Instancja modelu
        self.view_class_ref = view_class_ref
        self.view = None    # Instancja widoku, later
        self.current_question_obj = None  #  pytania
        self.time_limit_per_question = 0  # limit czasu
        self.player_name_for_save = ""   # Imię gracza 

    def set_view(self, view_instance):
        """
        Ustawia instancję View for Controller.
        """
        self.view = view_instance

    def get_categories(self):
        """
        Kategorii z Model.
        """
        return self.model.get_categories()

    def start_quiz(self):
    
        if not self.view:
            return  

        player_name = self.view.get_player_name()
        if not player_name:
            # Brak imienia
            return

        # Zapisz imię  dla wyniku
        self.player_name_for_save = player_name
        category = self.view.get_selected_category()

        # Sprawdzenie czy pytania zapisane
        if category is None and not self.model.all_questions:
            self.view.show_message(
                "Błąd Quizu", "Brak pytań w bazie. Sprawdź plik questions.json.", type="error")
            return
        if category == "Brak kategorii":  
            self.view.show_message(
                "Informacja", "Wybierz dostępną kategorię lub 'Wszystkie', aby rozpocząć.", type="info")
            return

        self.time_limit_per_question = self.view.get_time_limit()

        # Start QUIZu
        self.current_question_obj = self.model.start_quiz(category)

        if self.current_question_obj:
    
            self.view.show_question_screen(
                self.current_question_obj,
                self.model.current_question_index,  # Current question
                self.model.get_total_questions_in_current_quiz(),  
                self.time_limit_per_question  
            )
        else:
            # Brak pytan 
            error_msg = "Nie udało się załadować pytań. "
            if not self.model.all_questions:
                error_msg += "Plik questions.json jest pusty, nie istnieje lub ma nieprawidłowy format."
            elif category and category != "Wszystkie":
                error_msg += f"Brak pytań w kategorii '{category}'."
            else:
                error_msg += "Sprawdź plik questions.json i wybraną kategorię."
            self.view.show_message("Błąd Quizu", error_msg, type="error")
            self.view.show_start_screen()  #  ekran startowy powrot

    def time_up(self):

        if not self.view or not self.current_question_obj:
            return
        if self.view.next_question_button and self.view.next_question_button.cget('state') == 'disabled':
            self.model.submit_answer(
                self.current_question_obj, -1)  # -1 oznacza timeout
            # feedback dla timeout
            self.view.show_feedback(
                False, -1, self.current_question_obj.correct_answer_index)
            #  "Następne pytanie"
            self.view.next_question_button.config(state="normal")
            for btn in self.view.answer_buttons: 
                btn.config(state="disabled")

    def submit_answer(self, question_obj, selected_index):
        """
        :param question_obj: Aktualny obiekt pytania.
        :param selected_index: Indeks wybranej odpowiedzi.
        :return: True jeśli odpowiedź poprawna, False w przeciwnym razie.
        """
        if not self.view:
            return False
        is_correct = self.model.submit_answer(question_obj, selected_index)
        return is_correct

    def next_question(self):
        if not self.view:
            return

        self.current_question_obj = self.model.get_next_question()
        if self.current_question_obj:
            #  następne pytanie
            self.view.show_question_screen(
                self.current_question_obj,
                self.model.current_question_index,
                self.model.get_total_questions_in_current_quiz(),
                self.time_limit_per_question
            )
        else:
            # Koniec quizu 
            final_results = self.model.get_final_results()
            self.view.show_final_score_screen(final_results)

    def save_score(self):
        if not self.view:
            return

        if self.player_name_for_save:  
            if self.model.save_result(self.player_name_for_save):
                self.view.update_final_score_feedback(
                    f"Wynik dla '{self.player_name_for_save}' został zapisany!", "green")
            else:
                self.view.update_final_score_feedback(
                    "Błąd podczas zapisu wyniku. Sprawdź konsolę.", "red")
        else:
            self.view.update_final_score_feedback(
                "Nie można zapisać wyniku - brak imienia gracza.", "orange")

    def show_results_history(self):
        if not self.view:
            return
        history = self.model.load_results()
        self.view.show_results_history_screen(history)
