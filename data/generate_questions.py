import json
import random

# Define categories
categories = {
    "Historia": [
        "W którym roku rozpoczęła się II Wojna Światowa?",
        "Kto był pierwszym prezydentem USA?",
        "Który faraon wybudował Wielką Piramidę w Gizie?",
        "Jaki był cel wyprawy Krzysztofa Kolumba?",
        "Jakie państwo jako pierwsze ogłosiło niepodległość?",
        "Kiedy upadło Cesarstwo Rzymskie?",
        "Kim był Napoleon Bonaparte?",
        "Jak nazywał się pierwszy człowiek w kosmosie?",
        "Gdzie podpisano Deklarację Niepodległości USA?",
        "Która wojna zakończyła się w 1918 roku?"
    ],
    "Nauka": [
        "Co odkrył Albert Einstein?",
        "Jaką jednostkę miary używa się do mierzenia energii?",
        "Co to jest fotosynteza?",
        "Który pierwiastek chemiczny ma symbol 'O'?",
        "Jaka planeta jest największa w Układzie Słonecznym?",
        "Co to jest czarna dziura?",
        "Jak działa zasada Archimedesa?",
        "Kto wynalazł żarówkę?",
        "Co to jest DNA?",
        "Jaka jest prędkość światła w próżni?"
    ],
    "Kultura": [
        "Kto napisał 'Pan Tadeusz'?",
        "Który artysta stworzył obraz Mona Lisa?",
        "Jakie miasto jest znane z opery La Scala?",
        "Co to jest balet?",
        "Kto był twórcą filmu 'Gwiezdne Wojny'?",
        "Jaka jest stolica mody?",
        "Która książka J.R.R. Tolkiena została zekranizowana jako trylogia?",
        "Co to jest haiku?",
        "Kto napisał 'Romeo i Julia'?",
        "Jak nazywał się słynny kompozytor 'Dziadka do orzechów'?"
    ]
}

# Function to generate random answers
def generate_answers(correct):
    wrong_answers = [correct + str(i) for i in range(1, 4)]
    all_answers = wrong_answers + [correct]
    random.shuffle(all_answers)
    return all_answers

# Generate questions data
quiz_data = {}
for category, questions in categories.items():
    quiz_data[category] = []
    for question in questions:
        correct_answer = question.split()[0]  # Simplified logic
        quiz_data[category].append({
            "question": question,
            "answers": generate_answers(correct_answer),
            "correct_answer": correct_answer
        })

# Save to JSON file
with open("data/questions.json", "w", encoding="utf-8") as file:
    json.dump(quiz_data, file, ensure_ascii=False, indent=4)

print("Pytania zostały wygenerowane i zapisane do questions.json!")