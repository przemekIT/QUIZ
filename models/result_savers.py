import csv
import os
from datetime import datetime

def save_result(player_name, score, total_questions, quiz_time):
    file_path = "results/quiz_results.csv"
    
    # Ensure the results folder exists
    os.makedirs("results", exist_ok=True)

    # Prepare data for saving
    percentage = (score/total_questions) * 100
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save to CSV file 
    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # if file is empty, add a header row

        if file.tell() == 0:
            writer.writerow(["Imię gracza", "Data", "Wynik (%)", "Poprawne odpowiedzi", "Łączna liczba pytań", "Czas quizu"])

        writer.writerow([player_name, date_time, f"{percentage:.2f}%", score, total_questions, f"{quiz_time} sek"])

    print(f"Wynik zapisano do {file_path}")