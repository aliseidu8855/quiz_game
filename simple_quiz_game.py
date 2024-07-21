"""
Skills: Functions, loops, error handling.
Description: Build a quiz game that asks users multiple-choice questions.
Provide feedback on correct/incorrect answers and keep score.
"""
import requests
import random

class QuizGame:
    def __init__(self):
        self.questions = []
        self.score = 0
        self.load_questions()

    def get_difficulty_and_category(self):
        difficulty_map = {
            '1': 'easy',
            '2': 'medium',
            '3': 'hard'
        }
        
        categories_map = {
            'easy': {
                '1': 23,  # History
                '2': 22,  # Geography
                '3': 11   # Entertainment: Film
            },
            'medium': {
                '1': 20,  # Mythology
                '2': 23,  # History
                '3': 11,  # Entertainment: Film
                '4': 22   # Geography
            },
            'hard': {
                '1': 17,  # Science & Nature
                '2': 18   # Science: Computers
            }
        }
        
        while True:
            print("Choose difficulty level:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            difficulty_choice = input("Enter the number corresponding to your choice: ").strip()
            if difficulty_choice in difficulty_map:
                difficulty = difficulty_map[difficulty_choice]
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        
        print(f"Available categories for {difficulty} difficulty:")
        categories = categories_map[difficulty]
        for key, value in categories.items():
            print(f"{key}. {value}")
        
        category_choice = input("Enter the number corresponding to your choice (leave blank for any category): ").strip()
        if category_choice in categories:
            category = categories[category_choice]
        elif category_choice == "":
            category = None
        else:
            print("Invalid choice. Defaulting to any category.")
            category = None
        
        return difficulty, category

    def fetch_results(self, amount=50, difficulty=None, category=None):
        url = f"https://opentdb.com/api.php?amount={amount}&type=multiple"
        if difficulty:
            url += f"&difficulty={difficulty}"
        if category:
            url += f"&category={category}"
        response = requests.get(url)
        data = response.json()
        return data['results']

    def load_questions(self):
        difficulty, category = self.get_difficulty_and_category()
        try:
            questions = self.fetch_results(difficulty=difficulty, category=category)
            if not questions:
                raise ValueError("No questions found for the selected difficulty and category.")
            
            selected_questions = random.sample(questions, 5)  # Select 5 random questions
            
            for q in selected_questions:
                options = [
                    q['correct_answer'],
                    q['incorrect_answers'][0],
                    q['incorrect_answers'][1],
                    q['incorrect_answers'][2]
                ]
                
                random.shuffle(options)  # Shuffle the options
                
                formatted_question = {
                    "question": q['question'],
                    "options": [
                        f"A. {options[0]}",
                        f"B. {options[1]}",
                        f"C. {options[2]}",
                        f"D. {options[3]}"
                    ],
                    "answer": chr(options.index(q['correct_answer']) + 65)  # Find the correct answer's new position
                }
                self.questions.append(formatted_question)
        except Exception as e:
            print(f"An error occurred while loading questions: {e}")

    def ask_question(self, question):
        print(question["question"])
        for option in question["options"]:
            print(option)
        
        user_answer = None
        while user_answer not in ['A', 'B', 'C', 'D']:
            user_answer = input("Your answer (A, B, C, or D): ").strip().upper()
        
        correct_answer = question["answer"]
        if user_answer == correct_answer:
            print(f"{correct_answer} is Correct!\n")
            self.score += 1
        else:
            print(f"Incorrect. The correct answer was {correct_answer}.\n")

    def play(self):
        for question in self.questions:
            self.ask_question(question)
        print(f"Your final score is: {self.score}/{len(self.questions)}")

def main():
    game = QuizGame()
    game.play()

if __name__ == "__main__":
    main()







