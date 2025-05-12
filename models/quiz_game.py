import threading

class QuizGame:
    """Handles quiz logic separately from the UI"""
    def __init__(self, questions):
        self.questions = questions
        self.current_question_index = 0
        self.score = 0
        self.time_left = 15 

        self.timer_running = False

    def get_current_question(self):
        """Returns the current question data."""
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None
    
    def check_answer(self, selected_answer):
        correct_answer = self.questions[self.current_question_index]["correct_answer"]
        if selected_answer == correct_answer:
            self.score +=1
            return True
        return False
    
    def next_question(self):
        if self.current_question_index + 1 < len(self.questions):
            self.current_question_index += 1
            self.reset_timer()
            return True    # Indicates more questions exist

        return False       # Quiz is over 
    
    def get_score(self):
        """Returns the final quiz score."""
        return self.score


    def start_timer(self, update_ui_callback, disable_buttons_callback, show_next_button_callback):
        """Starts the countdown timer in the model."""
        if self.timer_running:  #  Prevent multiple timers
            return  

        self.timer_running = True  
        self.disable_buttons_callback = disable_buttons_callback # store callback for later use
        self.show_next_button_callback = show_next_button_callback

        def countdown():
            update_ui_callback(self.time_left)

            while self.time_left > 0 and self.timer_running:
                threading.Event().wait(1)
                self.time_left -= 1
                update_ui_callback(self.time_left)  #  Update UI in QuizScreen

            if self.time_left == 0 and self.timer_running:
                update_ui_callback(self.time_left)  # Final UI update
                self.auto_submit()  

        threading.Thread(target=countdown, daemon=True).start()  # Ensures timer runs in background

    def reset_timer(self):
        """Resets the countdown timer for a new question. """
        self.time_left = 15

    def stop_timer(self):
        """Stops the countdown timer."""
        self.timer_running = False

    def auto_submit(self):
        """Automatically submits an answer when time runs out and disables buttons."""
        if self.current_question_index < len(self.questions):            
            self.check_answer(None)  # Handles case where user didn't select an answer in time 

            if hasattr(self, "disable_buttons_callback"):
                self.disable_buttons_callback() # Inform UI to disable the buttons 

            if hasattr(self, "show_next_button_callback"):
                self.show_next_button_callback()  # Ensure "Next Question" button is active