import json
import os

def save_result(player_name, score, total_questions, quiz_time, category):
    """Save quiz results in the results folder."""
    
    # ✅ Define the correct directory path
    results_dir = "results"
    results_file = os.path.join(results_dir, "quiz_results.json")

    # ✅ Ensure the folder exists before saving
    os.makedirs(results_dir, exist_ok=True)

    result_data = {
        "name": player_name,
        "score": score,
        "total": total_questions,
        "time": quiz_time, 
        "category": category
    }
    
    try:
        with open(results_file, "r") as file:
            results = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        results = []

    results.append(result_data)

    with open(results_file, "w") as file:
        json.dump(results, file, indent=4)

    print(f" Wynik zapisano w: {results_file}")