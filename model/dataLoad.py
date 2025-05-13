import json
import csv
import os
import glob
from datetime import datetime
from model.question import Question
from pathlib import Path

class DataLoader:

    @staticmethod
    def load_questions_from_folder(folder_path):
        questions_by_category = {}
        category_names = []

        basePath = Path(__file__).parent
        file_path = (basePath / ".." / folder_path ).resolve()

        json_files = glob.glob(os.path.join(file_path, '*.json'))

        for file_path in json_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for category, items in data.items():
                questions = []
                for item in items:
                    text = item['question']
                    options = [opt['answer'] for opt in item['options']]

                    correct_index = next(i for i, opt in enumerate(item['options']) if opt['correct'] is True)
                    correct_answer_text = item['options'][correct_index]['answer']

                    question = Question(
                        text=text,
                        options=options,
                        correct_answer=correct_answer_text,
                        category=category
                    )
                    questions.append(question)

                questions_by_category[category] = questions
                category_names.append(category)

        return questions_by_category, category_names

    @staticmethod
    def save_result(filepath, player_name, score, total, time_elapsed):
        basePath = Path(__file__).parent
        file_path = (basePath / ".." / filepath ).resolve()

        with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                player_name,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                f"{score}/{total}",
                f"{time_elapsed:.2f}s"
            ])
            csvfile.flush()
