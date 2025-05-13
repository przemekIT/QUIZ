# quiz_app/main.py
import tkinter as tk
from model import QuizModel
from view import QuizView        
from controller import QuizController
import os                         # ścieżka pliku
import json                       # Przykladowy plik JSON


def ensure_questions_file_exists(file_path="questions.json"):
    if not os.path.exists(file_path):
        print(f"Plik {file_path} nie istnieje. Tworzenie przykładowego pliku...")
        example_questions = [
            {
                "text": "Stolicą Polski jest:",
                "answers": ["Kraków", "Gdańsk", "Warszawa", "Poznań"],
                "correct_answer_index": 2,
                "category": "Geografia"
            },
            {
                "text": "Ile wynosi 2 + 2 * 2?",
                "answers": ["4", "6", "8", "2"],
                "correct_answer_index": 1,
                "category": "Matematyka"
            },
            {
                "text": "Kto jest autorem 'Pana Tadeusza'?",
                "answers": ["Juliusz Słowacki", "Adam Mickiewicz", "Henryk Sienkiewicz", "Bolesław Prus"],
                "correct_answer_index": 1,
                "category": "Literatura"
            }
        ]
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(example_questions, f, indent=4, ensure_ascii=False)
            print(
                f"Utworzono przykładowy plik {file_path}. Uzupełnij go własnymi pytaniami.")
        except IOError as e:
            print(f"Krytyczny błąd: Nie można utworzyć pliku {file_path}: {e}")
        return False 
    return True 


if __name__ == "__main__":
    questions_file_path = "questions.json"
    results_file_path = "results.csv" #zapisanie wynikow

    ensure_questions_file_exists(questions_file_path)

    # Inicjalizacja głównego okna Tkinter
    root = tk.Tk()


    quiz_model = QuizModel(
        questions_file=questions_file_path, results_file=results_file_path)

    quiz_controller = QuizController(model=quiz_model, view_class_ref=QuizView)

    quiz_view = QuizView(root, quiz_controller)

    quiz_controller.set_view(quiz_view)

    if not quiz_model.all_questions:
        print("Uwaga: Nie załadowano żadnych pytań z pliku questions.json. "
              "Quiz może nie działać poprawnie lub nie wyświetlać żadnych pytań.")

    elif not quiz_controller.get_categories():
        print("Uwaga: Załadowano pytania, ale nie znaleziono żadnych unikalnych kategorii. "
              "Sprawdź poprawność danych w pliku questions.json.")

    # Uruchomienie głównej pętli Tkinter
    root.mainloop()
