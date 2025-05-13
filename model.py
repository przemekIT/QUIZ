# quiz_app/model.py
import json
import csv
import random
from datetime import datetime


class Question:


    def __init__(self, text, answers, correct_answer_index, category):
        self.text = text 
        self.answers = answers  
        self.correct_answer_index = correct_answer_index 
        self.category = category  

    def check_answer(self, user_answer_index):

        return user_answer_index == self.correct_answer_index


class QuizModel:


    def __init__(self, questions_file='questions.json', results_file='results.csv'):
        self.questions_file = questions_file  
        self.results_file = results_file   
        self.all_questions = self._load_questions()  
        self.current_questions = []  
        self.current_question_index = 0  # Bierzace pytanie
        self.score = 0  # wynik gracza
        self.quiz_start_time = None  
        self.quiz_end_time = None   

    def _load_questions(self):
        """
        Wczytuje pytania z pliku JSON.
        """
        try:
            with open(self.questions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                questions = []
                for q_data in data:
                    questions.append(Question(
                        q_data['text'],
                        q_data['answers'],
                        q_data['correct_answer_index'],
                        q_data['category']
                    ))
                return questions
        except FileNotFoundError:
            print(f"Błąd: Plik {self.questions_file} nie został znaleziony.")
            return []
        except json.JSONDecodeError:
            print(
                f"Błąd: Nieprawidłowy format pliku JSON w {self.questions_file}.")
            return []
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd podczas ładowania pytań: {e}")
            return []

    def get_categories(self):

        if not self.all_questions:
            return []
        categories = set()
        for question in self.all_questions:
            categories.add(question.category)
        return sorted(list(categories))

    def start_quiz(self, category=None, num_questions=10):

        self.score = 0
        self.current_question_index = 0
        self.quiz_start_time = datetime.now()
        self.quiz_end_time = None

        if not self.all_questions:
            return None

        if category and category != "Wszystkie":
            self.current_questions = [
                q for q in self.all_questions if q.category == category]
        else:
            self.current_questions = list(self.all_questions)  # Kopia listy

        if not self.current_questions:
            return None

        random.shuffle(self.current_questions)
        # Mozna ograniczyc ilosc pytań, jeśli jest ich więcej niż num_questions
        if len(self.current_questions) > num_questions:
            self.current_questions = self.current_questions[:num_questions]

        return self.get_next_question()

    def get_next_question(self):

        if self.current_question_index < len(self.current_questions):
            question = self.current_questions[self.current_question_index]
            self.current_question_index += 1
            return question
        else:
            # czas zakończenia, gdy pytania się skończą
            self.quiz_end_time = datetime.now()
            return None

    def submit_answer(self, question, user_answer_index):

        if user_answer_index == -1:  # Czas minął lub brak odpowiedzi
            return False
        if question.check_answer(user_answer_index):
            self.score += 1
            return True
        return False

    def get_current_score(self):

        return self.score

    def get_total_questions_in_current_quiz(self):

        return len(self.current_questions)

    def get_final_results(self):

        total_questions = self.get_total_questions_in_current_quiz()
        if total_questions == 0:
            percentage = 0.0
        else:
            percentage = (self.score / total_questions) * 100

        comment = ""
        if percentage == 100:
            comment = "Świetnie!"
        elif percentage >= 75:
            comment = "Bardzo dobrze!"
        elif percentage >= 50:
            comment = "Nieźle, ale możesz lepiej!"
        else:
            comment = "Spróbuj ponownie!"

        quiz_duration_seconds = 0
        if self.quiz_start_time and self.quiz_end_time:
            quiz_duration = self.quiz_end_time - self.quiz_start_time
            quiz_duration_seconds = quiz_duration.total_seconds()
        # Na wypadek, gdyby quiz nie zakończył się normalnie
        elif self.quiz_start_time and not self.quiz_end_time:
            quiz_duration_seconds = (
                datetime.now() - self.quiz_start_time).total_seconds()

        return {
            "score": self.score,
            "total_questions": total_questions,
            "percentage": round(percentage, 2),
            "comment": comment,
            "duration_seconds": round(quiz_duration_seconds, 2)
        }

    def save_result(self, player_name):

        results_data = self.get_final_results()
        try:
            file_exists_and_has_content = False
            try:
                with open(self.results_file, 'r', newline='', encoding='utf-8') as f_check:
                    if f_check.read(1):  # Sprawdźenie, czy plik nie jest pusty
                        file_exists_and_has_content = True
            except FileNotFoundError:
                pass  # Plik nie istnieje, zostanie utworzony

            with open(self.results_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists_and_has_content:
                    writer.writerow(
                        ["Imię gracza", "Data", "Wynik", "Procent (%)", "Czas quizu (s)"])
                writer.writerow([
                    player_name,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    f"{results_data['score']}/{results_data['total_questions']}",
                    f"{results_data['percentage']}",
                    results_data['duration_seconds']
                ])
            print(f"Wynik zapisany dla {player_name} w {self.results_file}")
            return True
        except IOError as e:
            print(
                f"Błąd: Nie można zapisać wyniku do pliku {self.results_file}. {e}")
            return False
        except Exception as e:
            print(f"Nieoczekiwany błąd podczas zapisu wyniku: {e}")
            return False

    def load_results(self):

        results_history = []
        try:
            with open(self.results_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None) 
                if header:
                    for row in reader:
                        if len(row) == len(header):  
                            results_history.append(row)
                        else:
                            print(
                                f"Pominięto nieprawidłowy wiersz w historii wyników: {row}")
            return results_history
        except FileNotFoundError:
    
            return []
        except Exception as e:
            print(f"Błąd podczas wczytywania historii wyników: {e}")
            return []
