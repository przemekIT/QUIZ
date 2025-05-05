import json

def load_questions(category):
    try:
        with open("data/questions.json", "r", encoding="utf-8") as file:
            questions_data = json.load(file)
            return questions_data.get(category, [])
    except(FileNotFoundError, json.JSONDecodeError):
        print("Błąd: Nie można wczytać pliky z pytaniami.")
        return []