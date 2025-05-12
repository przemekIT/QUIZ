from models.result_manager import ResultManager
import tkinter as tk
from tkinter import ttk

class ResultHistoryScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Historia wyników")
        self.geometry("600x400")

        self.result_manager = ResultManager()  

        # Sorting attributes
        self.current_sort_column = "score"   # Default sorting column
        self.sort_order = False              # False = Descending (Highest first),  True = Ascending

        # Apply Treeview Styles for Headers 
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="blue")  # Bold & blue headers
        style.configure("Treeview", rowheight=25)  # Adjust row height for better spacing

        self.create_widgets()
        self.load_results()

    def create_widgets(self):
        self.title_label = ttk.Label(self, text="Historia wyników", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)

        # Treeview (Table) to Display Results
        self.results_tree = ttk.Treeview(self, columns=("Name", "Category", "Score", "Total"), show="headings")
        self.results_tree.pack(fill="both", expand=True)

        # Define Column Headers with Clickable Sorting (Total has disable sorting)
        self.results_tree.heading("Name", text="Name", command=lambda: self.sort_results("name"))
        self.results_tree.heading("Category", text="Category", command=lambda: self.sort_results("category"))
        self.results_tree.heading("Score", text="Score", command=lambda: self.sort_results("score"))
        self.results_tree.heading("Total", text="Total")  # Keeps header visible but removes sorting

        # Set Default Column Width
        self.results_tree.column("Name", width=150)
        self.results_tree.column("Category", width=100)
        self.results_tree.column("Score", width=60)
        self.results_tree.column("Total", width=60)

    def load_results(self):
        """Loads and populates results into the Treeview table."""
        self.update_results()

    def update_results(self, event=None):
        """Filters and sorts quiz results dynamically."""
        selected_category = None
        entered_name = None

        results = self.result_manager.filter_results(category=selected_category, player_name=entered_name)

        # Check if the current_sort_column exists in result before sorting
        if results and self.current_sort_column in results[0]:  
            results.sort(key=lambda x: x[self.current_sort_column], reverse=not self.sort_order)
        else:
            print(f"Warning: '{self.current_sort_column}' not found in result data.")  # Debugging step

        # Clear previous results before inserting new ones
        for row in self.results_tree.get_children():
            self.results_tree.delete(row)

        # Insert filtered results into the Treeview
        for result in results:
            self.results_tree.insert("", "end", values=(result["name"], result["category"], result["score"], result["total"]))

    def sort_results(self, column):
        """Toggles sorting order when clicking column headers."""
        self.current_sort_column = column.lower()
        self.sort_order = not self.sort_order  # Toggle between ascending/descending
        self.update_results()  # Refresh results with new sorting order