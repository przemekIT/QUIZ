import json
import random

def load_questions(category):
    """Loads questions from a specific category."""
    try:
        with open("data/questions.json", "r", encoding="utf-8") as file:
            questions_data = json.load(file)
            return questions_data.get(category, [])
    except(FileNotFoundError, json.JSONDecodeError):
        print("Błąd: Nie można wczytać pliky z pytaniami.")
        return []
    
def load_random_questions():
    """Loads random questions from all available categories. """
    try:
        with open("data/questions.json", "r", encoding="utf-8") as file:
            questions_data = json.load(file)

            all_questions = []
            for category in questions_data.keys(): 
                all_questions.extend(questions_data[category])
            
            random.shuffle(all_questions) # Shuffle the mixed questions set 

            return random.sample(all_questions, min(len(all_questions), 20)) 
    except:
        print("Błąd: Nie można wczytać pliky z pytaniami.")
        return []

