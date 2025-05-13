class Question:
    def __init__(self, text, options, correct_answer, category):
        self.text = text
        self.options = options  # list [A, B, C, D]
        self.correct_answer = correct_answer  # "A", "B", etc.
        self.category = category
