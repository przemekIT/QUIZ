import json
import os

class ResultManager:
    """Handles quiz results storage and filtering logic."""

    def __init__(self, file_path="results/quiz_results.json"):
        self.file_path = file_path

    def load_results(self):
        """Loads saved quiz results and sorts them by score."""
        if not os.path.exists(self.file_path):
            return []
        
        try:
            with open(self.file_path, "r") as file:
                results = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            results = []

        # Sort results from highest to lowest score

        results.sort(key=lambda x: x["score"], reverse=True)
        return results 
    
    def get_unique_categories(self):
        """Extracts unique categories from results."""
        results = self.load_results()
        categories = {result["category"] for result in results}
        return sorted(categories)
    
    def filter_results(self, category=None, player_name=None):
        """Filters results by category and player name."""
        results = self.load_results()
        filtered = []

        for result in results:
            if (category is None or result["category"] == category and (player_name is None or player_name.lower() in result["name"].lower())):
                filtered.append(result)
    
        return filtered
        
    def update_results(self, event=None):
        """Filters and sorts quiz results dynamically, then updates the table."""
        selected_category = self.category_filter.get()
        entered_name = self.name_filter.get().strip()

        filtered_results = self.result_manager.filter_results(
            category=None if selected_category == "All" else selected_category,
            player_name=entered_name if entered_name else None
        )

        # Clear previous rows before inserting new ones
        for row in self.results_tree.get_children():
            self.results_tree.delete(row)

        # Insert filtered results into the Treeview
        for result in filtered_results:
            self.results_tree.insert("", "end", values=(result["name"], result["category"], result["score"], result["total"]))