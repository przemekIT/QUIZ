import json
import csv
import random
from datetime import datetime

# Zarządza danymi (pytania ,wątki)

class QuizData:
    def __init__(self, filepath='data/pytania.json'):
        self.filepath = filepath
        self.questions = self.load_questions()

    def load_questions(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_random_question(self):
        return random.choice(self.questions)

    def save_result(self, name, age, score, time_taken):
        with open('data/wyniki.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([name, age, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), score, time_taken])

