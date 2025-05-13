import random

class Quiz:
    def __init__(self, questions):
        self.questions = random.sample(questions, k=len(questions))
        self.current_index = 0
        self.correct_count = 0

    def current_question(self):
        return self.questions[self.current_index]

    def get_current_question(self):
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def answer_current(self, selected_option):
        current = self.current_question()
        
        is_correct = (current.correct_answer == selected_option)

        if is_correct:
            self.correct_count += 1
        self.current_index += 1
        return is_correct


    def is_finished(self):
        return self.current_index >= len(self.questions)

    def total_questions(self):
        return len(self.questions)