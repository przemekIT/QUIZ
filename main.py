# Główna logika aplikacji: łączenie kontrolera i widoku
from controller.quiz_controller import QuizController


def start_app():
    app = QuizController()
    app.run()

if __name__ == "__main__":
    start_app()
